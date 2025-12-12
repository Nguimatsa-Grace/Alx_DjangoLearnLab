# notifications/views.py (COMPLETE AND CONFIRMED CORRECT FIX)

from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import Q # Ensure Q is imported for complex lookups


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing and listing notifications.
    Uses ReadOnlyModelViewSet as users should not create/update notifications directly.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Correct the queryset to filter for the currently authenticated user
    # and use the correct ordering field 'timestamp'
    def get_queryset(self):
        # Filter notifications where the authenticated user is the recipient
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)

        # Apply ordering using the correct field 'timestamp'
        # The '-timestamp' means descending order (newest first)
        queryset = queryset.order_by('-timestamp')

        # Optional: Allow filtering by unread status
        unread_status = self.request.query_params.get('unread')
        if unread_status is not None:
            if unread_status.lower() == 'true':
                # The model field is 'unread'
                queryset = queryset.filter(unread=True)
            elif unread_status.lower() == 'false':
                queryset = queryset.filter(unread=False)

        return queryset