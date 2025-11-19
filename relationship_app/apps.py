# relationship_app/apps.py

from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # The 'name' must match the folder name:
    name = 'relationship_app'