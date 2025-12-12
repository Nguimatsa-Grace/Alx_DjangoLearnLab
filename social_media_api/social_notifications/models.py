# social_notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications'
    )
    verb = models.CharField(max_length=255)
    
    # Generic Foreign Key setup:
    # 1. content_type (links to the model type, e.g., Post, Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2. object_id (the primary key of the target object)
    object_id = models.PositiveIntegerField()
    # 3. target (the actual field that provides the related object instance)
    target = GenericForeignKey('content_type', 'object_id')
    

    # Status fields
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target}'
