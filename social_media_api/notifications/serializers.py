# notifications/serializers.py

from rest_framework import serializers
from .models import Notification
from accounts.serializers import CustomUserSerializer  # Ensure this import is correct

class NotificationSerializer(serializers.ModelSerializer):
    recipient = CustomUserSerializer(read_only=True)
    actor = CustomUserSerializer(read_only=True)
    target_object_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 
            'recipient', 
            'actor', 
            'verb', 
            'unread', 
            'timestamp', # <--- CORRECT FIELD: 'timestamp'
            'content_type',
            'object_id',
            'target_object_str',
        )
        # Use 'timestamp' here as well
        read_only_fields = ('recipient', 'actor', 'timestamp', 'content_type', 'object_id') 

    def get_target_object_str(self, obj):
        if obj.content_object:
            if obj.content_object.__class__.__name__ == 'Post':
                # Safely attempt to get the title or just use the object string
                return f"Post: '{getattr(obj.content_object, 'title', str(obj.content_object))}'"
            return str(obj.content_object)
        return "Unknown Target"