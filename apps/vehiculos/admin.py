from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'locality', 'applicant', 'created_at')
    search_fields = ('brand', 'locality', 'applicant')