from datetime import datetime
from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    # def ready(self):
    #     from user.models import CustomUser
    #     for user in list(CustomUser.objects.all()):
    #         user.delete()
        
    