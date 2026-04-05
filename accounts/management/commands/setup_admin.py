import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea el superusuario inicial y el grupo Administrador con todos los permisos.'

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name='administrador')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{admin_group.name}" creado.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Grupo "{admin_group.name}" ya existe.'))
        
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS(f'Se han asignado {permissions.count()} permisos al grupo "{admin_group.name}".'))

        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        document = os.environ.get('DJANGO_SUPERUSER_DOCUMENT')

        if not email or not password or not document:
            self.stdout.write(self.style.WARNING('Faltan variables de entorno para el superusuario. Saltando creación.'))
            return

        if not User.objects.filter(email=email).exists():
            self.stdout.write(f'Creando superusuario para {email}...')
            User.objects.create_superuser(
                email=email,
                password=password,
                document_number=document
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario {email} creado correctamente.'))
            
            user = User.objects.get(email=email)
            user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Superusuario {email} añadido al grupo "{admin_group.name}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuario {email} ya existe.'))
