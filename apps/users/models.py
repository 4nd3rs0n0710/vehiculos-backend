from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    
    Agrega el campo `role` para el control de acceso basado en roles (RBAC).
    - admin: acceso completo al CRUD
    - viewer: solo lectura
    
    El campo email tiene restricción unique para evitar registros duplicados.
    """

    class Role(models.TextChoices):
        ADMIN  = 'admin',  'Admin'
        VIEWER = 'viewer', 'Viewer'

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER,
        verbose_name="Rol",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        """Retorna True si el usuario tiene rol de administrador."""
        return self.role == self.Role.ADMIN