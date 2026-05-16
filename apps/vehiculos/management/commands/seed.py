from django.core.management.base import BaseCommand
from apps.vehiculos.models import Vehicle
from apps.users.models import User


VEHICLES = [
    {"brand": "Toyota", "locality": "Bogotá", "applicant": "Carlos Ramírez"},
    {"brand": "Mazda", "locality": "Medellín", "applicant": "Laura Gómez"},
    {"brand": "Chevrolet", "locality": "Cali", "applicant": "Andrés Torres"},
    {"brand": "Renault", "locality": "Barranquilla", "applicant": "María Pérez"},
    {"brand": "Kia", "locality": "Bucaramanga", "applicant": "Jorge Díaz"},
]


class Command(BaseCommand):
    help = "Crea datos iniciales."

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', email='admin@test.com',
                password='Admin1234!', role='admin'
            )
            self.stdout.write(self.style.SUCCESS("Usuario admin creado"))

        if not User.objects.filter(username='viewer').exists():
            User.objects.create_user(
                username='viewer', email='viewer@test.com',
                password='Viewer1234!', role='viewer'
            )
            self.stdout.write(self.style.SUCCESS("Usuario viewer creado"))

        created = 0
        for v in VEHICLES:
            _, was_created = Vehicle.objects.get_or_create(**v)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} vehículos creados."))