# notifications/permissions.py (CREATE THIS FILE)

from rest_framework import permissions

class IsRecipientOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow recipients of an object to view/modify it.
    Read permissions are allowed to authenticated users if the permission check passes.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed if the user is the recipient
        if request.method in permissions.SAFE_METHODS:
            return obj.recipient == request.user

        # Write/Update permissions are only allowed to the recipient (for marking as read)
        return obj.recipient == request.user