"""
Commande de gestion pour créer le superutilisateur admin automatiquement.
Usage: python manage.py seed_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Crée ou met à jour le superutilisateur administrateur par défaut'

    def handle(self, *args, **options):
        username = settings.ADMIN_USERNAME
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )
        
        # Toujours mettre à jour le mot de passe pour qu'il corresponde aux .env
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Superutilisateur "{username}" créé.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Mot de passe du superutilisateur "{username}" mis à jour.'))
        
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Mot de passe: {password}')
