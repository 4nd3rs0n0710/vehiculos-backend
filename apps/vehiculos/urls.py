from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.vehiculos.views import VehicleViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehiculo')

urlpatterns = [
    path('', include(router.urls)),
]