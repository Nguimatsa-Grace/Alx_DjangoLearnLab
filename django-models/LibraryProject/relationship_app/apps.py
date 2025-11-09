# relationship_app/apps.py (RESTORED)

from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Ensure this is present if you removed it
    name = 'relationship_app'

    def ready(self):
        import relationship_app.signals