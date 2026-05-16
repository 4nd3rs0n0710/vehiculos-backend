from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.users.permissions import IsAdminOrReadOnly
from .models import Vehicle
from .serializers import VehicleSerializer
import structlog

logger = structlog.get_logger()


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("vehicle_created", id=instance.id, brand=instance.brand,
                    user=self.request.user.username)

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("vehicle_updated", id=instance.id, brand=instance.brand,
                    user=self.request.user.username)

    def perform_destroy(self, instance):
        logger.info("vehicle_deleted", id=instance.id, brand=instance.brand,
                    user=self.request.user.username)
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Vehículo '{instance.brand}' eliminado correctamente."},
            status=status.HTTP_200_OK
        )