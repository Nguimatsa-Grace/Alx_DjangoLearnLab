from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    # The default_auto_field is already set in project settings, but good practice to include
    default_auto_field = 'django.db.models.BigAutoField'
    
    # This is the short name of the app
    name = 'users'
    
    # This is the verbose name shown in the Django Admin
    verbose_name = _('Users') 

    def ready(self):
        # This is where you would import signals if you had them, 
        # but for now, we leave it empty.
        pass