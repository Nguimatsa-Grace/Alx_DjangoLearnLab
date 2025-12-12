# notifications/models.py (NEW Notification Model)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    Model to track notifications for user interactions.
    """
    # Who should receive the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        help_text='The user who should see this notification.'
    )
    
    # Who initiated the action (e.g., the user who liked the post)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='actions',
        help_text='The user who performed the action.'
    )
    
    # What the action was (e.g., 'followed', 'liked', 'commented')
    verb = models.CharField(max_length=255)
    
    # The object related to the action (Post, Like, Comment, User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target} for {self.recipient.username}'