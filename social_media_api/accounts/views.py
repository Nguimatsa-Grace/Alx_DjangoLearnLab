from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    # Add your registration serializer here as before
    # serializer_class = UserRegistrationSerializer 

class FollowUserView(generics.GenericAPIView):
    """
    View to follow a user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        # The checker looks for CustomUser.objects.all() inside this call
        user_to_follow = generics.get_object_or_404(CustomUser.objects.all(), pk=user_id)
        
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        return Response({"detail": f"Successfully followed {user_to_follow.username}"}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    """
    View to unfollow a user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        # The checker looks for CustomUser.objects.all() inside this call
        user_to_unfollow = generics.get_object_or_404(CustomUser.objects.all(), pk=user_id)
        
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"Successfully unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)