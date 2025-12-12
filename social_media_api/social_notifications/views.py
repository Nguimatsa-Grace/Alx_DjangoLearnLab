from rest_framework import generics, permissions
from .models import Notification
from accounts.serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    View to list notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Returns notifications where the current user is the recipient
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')