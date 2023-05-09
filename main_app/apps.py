from django.apps import AppConfig
from django.db.models.signals import post_save

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        from django.contrib.auth.models import User
        from main_app.views import create_profile
        
        # connect the create_profile signal to the User model
        post_save.connect(create_profile, sender=User)
