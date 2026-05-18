# 🚗 Vehicles Manager — Backend

API REST construida con **Django 5 + Django REST Framework** para gestión de vehículos de concesionario. Incluye autenticación JWT, control de acceso por roles (RBAC) y logging estructurado.

---

## 🛠 Stack

| Tecnología | Versión |
|---|---|
| Python | 3.12 |
| Django | 5.0.4 |
| Django REST Framework | 3.x |
| PostgreSQL | 16 |
| Docker / Docker Compose | — |
| djangorestframework-simplejwt | — |
| structlog | — |

---

## 📁 Estructura del proyecto

```
vehiculos-backend/
├── apps/
│   ├── users/           # Autenticación, registro, perfil, recuperación de contraseña
│   │   ├── models.py    # Modelo User con roles (admin/viewer)
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   └── urls.py
│   └── vehiculos/       # CRUD de vehículos
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── middleware.py    # Logging de peticiones HTTP
│   └── wsgi.py
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## 🔐 Autenticación y Seguridad

- **JWT** con access token (60 min) y refresh token (7 días)
- **Contraseñas** cifradas con PBKDF2-SHA256
- **RBAC** — dos roles definidos:
  - `admin`: acceso completo al CRUD
  - `viewer`: solo lectura (GET)
- **Límite de intentos**: 5 intentos fallidos bloquean el login por 5 minutos
- **Token de reset de contraseña**: válido por 24 horas, de un solo uso

---

## 📡 Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/auth/login/` | Login con email o username |
| POST | `/api/auth/refresh/` | Renovar access token |
| POST | `/api/auth/register/` | Registro de usuario |
| GET | `/api/auth/profile/` | Perfil del usuario autenticado |
| POST | `/api/auth/recovery/` | Envío de correo de recuperación |
| POST | `/api/auth/reset-password/` | Restablecer contraseña con token |

### Vehículos

| Método | Endpoint | Descripción | Rol requerido |
|---|---|---|---|
| GET | `/api/vehicles/` | Listar vehículos | viewer / admin |
| POST | `/api/vehicles/` | Crear vehículo | admin |
| PATCH | `/api/vehicles/{id}/` | Editar vehículo | admin |
| DELETE | `/api/vehicles/{id}/` | Eliminar vehículo | admin |

---

## 🚀 Instalación y ejecución local

### Requisitos previos

- Docker Desktop instalado y corriendo

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd vehiculos-project
```

2. Crear archivo `.env` en la raíz del proyecto:
```env
DJANGO_SECRET_KEY=tu-clave-secreta
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

POSTGRES_DB=vehicles_db
POSTGRES_USER=vehicles_user
POSTGRES_PASSWORD=vehicles_pass
DB_HOST=db
DB_PORT=5432

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

EMAIL_HOST_USER=tu-correo@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

3. Levantar los servicios:
```bash
docker-compose up
```

4. Aplicar migraciones:
```bash
docker-compose exec backend python manage.py migrate
```

5. Crear usuarios de prueba:
```bash
docker-compose exec backend python manage.py seed
```

### Usuarios por defecto

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | Admin1234! | admin |
| viewer | Viewer1234! | viewer |

---

## 📋 Logging

Cada petición HTTP es registrada con structlog incluyendo:
- Método HTTP
- URI
- Código de estado
- Tiempo de respuesta
- Usuario autenticado (si aplica)

---

## 🌐 Despliegue

El backend está desplegado en **Render**.

🔗 URL de producción: `<url-render>`