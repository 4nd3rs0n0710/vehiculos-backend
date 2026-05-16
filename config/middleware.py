import structlog
import time

# Logger configurado con structlog para salida estructurada
logger = structlog.get_logger()


class RequestLoggingMiddleware:
    """
    Middleware que registra cada request HTTP entrante.
    
    Registra: método, ruta, código de estado, duración en ms
    y el ID + rol del usuario si está autenticado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Marca el tiempo de inicio para calcular duración
        start = time.time()

        response = self.get_response(request)

        duration_ms = round((time.time() - start) * 1000, 2)

        # Determina si el usuario está autenticado para incluirlo en el log
        user_info = "anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = f"{request.user.id}:{request.user.role}"

        logger.info(
            "http_request",
            method=request.method,
            path=request.path,
            status=response.status_code,
            duration_ms=duration_ms,
            user=user_info,
        )
        return response