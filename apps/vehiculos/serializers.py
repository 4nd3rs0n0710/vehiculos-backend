from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'brand', 'locality', 'applicant', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_brand(self, value):
        if not value.strip():
            raise serializers.ValidationError("La marca no puede estar vacía.")
        return value.strip()

    def validate_locality(self, value):
        if not value.strip():
            raise serializers.ValidationError("La localidad no puede estar vacía.")
        return value.strip()

    def validate_applicant(self, value):
        if not value.strip():
            raise serializers.ValidationError("El aspirante no puede estar vacío.")
        return value.strip()