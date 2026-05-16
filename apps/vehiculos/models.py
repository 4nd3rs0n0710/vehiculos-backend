from django.db import models


class Vehicle(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Marca")
    locality = models.CharField(max_length=150, verbose_name="Localidad")
    applicant = models.CharField(max_length=200, verbose_name="Aspirante")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} — {self.locality} — {self.applicant}"