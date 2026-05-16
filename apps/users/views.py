from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import User
import structlog

logger = structlog.get_logger()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado que agrega el rol y username
    al payload del JWT y a la respuesta del login.
    
    Esto evita que el frontend tenga que hacer una segunda
    llamada para obtener el rol del usuario.
    """

    @classmethod
    def get_token(cls, user):
        # Agrega claims personalizados al token JWT
        token = super().get_token(user)
        token['role']     = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Incluye rol y username en la respuesta del login
        data['role']     = self.user.role
        data['username'] = self.user.username
        logger.info("user_login", username=self.user.username, role=self.user.role)
        return data


class LoginView(TokenObtainPairView):
    """Endpoint de login que retorna access token, refresh token y rol."""
    serializer_class = CustomTokenObtainPairSerializer


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