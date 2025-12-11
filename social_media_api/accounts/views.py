# accounts/views.py (FIXED IMPORTS)

from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework.decorators import action
from .serializers import (
    CustomUserRegistrationSerializer, 
    CustomUserLoginSerializer, 
    # ONLY import the necessary detail serializer
    CustomUserDetailSerializer
)
from .models import CustomUser

# --- ORIGINAL VIEWS (KEPT) ---

# API View for User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
# ... (rest of UserRegistrationView code is the same) ...

# API View for User Login and Token Retrieval
class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserLoginSerializer
# ... (rest of UserLoginView code is the same) ...

# API View for User Profile (Read/Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    # Now using the consolidated detail serializer
    serializer_class = CustomUserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,) 

    def get_object(self):
        return self.request.user

# --- NEW VIEWSET FOR FOLLOW/UNFOLLOW ---

class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for listing, retrieving users, and managing follow relationships.
    """
    queryset = CustomUser.objects.all().order_by('username')
    # Using the consolidated detail serializer
    serializer_class = CustomUserDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]
    
    # ... (rest of follow/unfollow actions are the same) ...

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        try:
            user_to_follow = self.get_object()
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.following.filter(pk=user_to_follow.pk).exists():
            return Response({'detail': f'You are already following {user_to_follow.username}.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({'detail': f'Successfully followed {user_to_follow.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        try:
            user_to_unfollow = self.get_object()
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.following.filter(pk=user_to_unfollow.pk).exists():
            return Response({'detail': f'You are not currently following {user_to_unfollow.username}.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'Successfully unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)