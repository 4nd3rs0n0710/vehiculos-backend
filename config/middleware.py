import structlog
import time

logger = structlog.get_logger()

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration_ms = round((time.time() - start) * 1000, 2)

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