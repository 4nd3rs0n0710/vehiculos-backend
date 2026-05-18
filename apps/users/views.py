from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from smtplib import SMTPAuthenticationError, SMTPException
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


from .serializers import RegisterSerializer, UserProfileSerializer
from .models import User
import structlog

logger = structlog.get_logger()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Permite login con email o username
        username_or_email = attrs.get('username', '')
        
        # Si contiene @ busca por email
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass

        data = super().validate(attrs)
        data['role']     = self.user.role
        data['username'] = self.user.username
        logger.info("user_login", username=self.user.username, role=self.user.role)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role']     = user.role
        token['username'] = user.username
        return token


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        cache_key = f'login_attempts_{username}'
        attempts = cache.get(cache_key, 0)

        # Bloquear si supera 5 intentos
        if attempts >= 5:
            return Response(
                {'detail': 'Cuenta bloqueada temporalmente. Intenta en 5 minutos.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Login exitoso — limpia el contador
            cache.delete(cache_key)
        else:
            # Login fallido — incrementa el contador (expira en 5 minutos)
            cache.set(cache_key, attempts + 1, timeout=300)

        return response


class RegisterView(generics.CreateAPIView):
    """Endpoint público para registrar nuevos usuarios."""
    queryset           = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class   = RegisterSerializer


class ProfileView(APIView):
    """Retorna los datos del usuario autenticado."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
class PasswordRecoveryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', '').strip()
        
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f'http://localhost:3000/reset-password?uid={uid}&token={token}'
            
            try:
                send_mail(
                    subject='Recuperación de contraseña — Monitoring Innovation',
                    message=f'Haz clic en el siguiente enlace para restablecer tu contraseña:\n\n{reset_url}\n\nEste enlace expira en 24 horas.',
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info("password_recovery_sent", email=email)
            except SMTPAuthenticationError:
                logger.error("smtp_auth_error", email=email)
            except SMTPException as e:
                logger.error("smtp_error", email=email, error=str(e))
                
        except User.DoesNotExist:
            logger.info("password_recovery_attempted", email=email)

        return Response(
            {'detail': 'Si el correo existe, recibirás un enlace de recuperación.'},
            status=status.HTTP_200_OK
        )

class ResetPasswordView(APIView):
    """Endpoint para restablecer la contraseña con el token del correo."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        uid      = request.data.get('uid', '')
        token    = request.data.get('token', '')
        password = request.data.get('password', '')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user    = User.objects.get(pk=user_id)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {'detail': 'El enlace es inválido o ha expirado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.save()
            logger.info("password_reset_success", username=user.username)
            return Response(
                {'detail': 'Contraseña restablecida exitosamente.'},
                status=status.HTTP_200_OK
            )
        except (User.DoesNotExist, ValueError):
            return Response(
                {'detail': 'El enlace es inválido o ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )