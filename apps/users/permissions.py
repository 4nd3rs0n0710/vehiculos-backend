from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permiso que solo permite acceso a usuarios con rol 'admin'.
    Retorna 403 Forbidden si el usuario es viewer o no está autenticado.
    """
    message = "Se requiere rol de administrador para esta acción."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Permiso mixto para el CRUD de vehículos:
    - Viewers pueden hacer GET (listar y ver detalle)
    - Solo admins pueden POST, PUT, PATCH, DELETE
    
    Retorna 401 si no está autenticado, 403 si no tiene el rol necesario.
    """

    def has_permission(self, request, view):
        # Rechaza usuarios no autenticados
        if not request.user or not request.user.is_authenticated:
            return False

        # Permite lectura a cualquier usuario autenticado
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Solo admins pueden modificar datos
        return request.user.role == 'admin'