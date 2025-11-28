from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to perform write operations (POST, PUT, DELETE).
    Read operations (GET, HEAD, OPTIONS) are allowed for all.
    """

    def has_permission(self, request, view):
        # Allow read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to staff users
        return request.user and request.user.is_staff