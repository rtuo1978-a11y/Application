from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from .auth import seed_admin
        try:
            seed_admin()
        except Exception as e:
            print(f'Erreur lors de l\'initialisation admin: {e}')
