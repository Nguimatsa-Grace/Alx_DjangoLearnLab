# accounts/views.py (FINAL FIXED VERSION - Fixing Serializer Import Mismatch)

from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType 

from .serializers import (
    # FIX: Use the correct names from accounts/serializers.py
    UserRegistrationSerializer,     # Corrected from CustomUserRegistrationSerializer
    CustomUserLoginSerializer,      # Assuming this name is correct for login
    CustomUserSerializer            # Corrected from CustomUserDetailSerializer
)
from .models import CustomUser
from notifications.models import Notification 

# --- ORIGINAL VIEWS (KEPT) ---

# API View for User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer # FIX: Use UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user) 
        response_data = serializer.data
        response_data['token'] = token.key
        return Response(response_data, status=status.HTTP_201_CREATED)

# API View for User Login and Token Retrieval
class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserLoginSerializer
    def post(self, request, *args, **kwargs):
        # NOTE: This line needs serializer_class to be set or passed in post() for validation to work,
        # but for the sake of getting the server running, we assume it's set in the class definition.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] 
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)

# API View for User Profile (Read/Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer # FIX: Use CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,) 
    def get_object(self):
        return self.request.user

# --- FOLLOW/UNFOLLOW VIEWS (UPDATED with explicit Notification logic) ---

class FollowUserView(generics.GenericAPIView):
    """
    Follow a user and creates a notification for the recipient.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all() 
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(pk=user_id) 
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if request.user.following.filter(pk=user_to_follow.pk).exists():
            return Response({'detail': f'You are already following {user_to_follow.username}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the following relationship
        request.user.following.add(user_to_follow)

        # --- TASK 3: CREATE FOLLOW NOTIFICATION (FIXED LOGIC) ---
        user_content_type = ContentType.objects.get_for_model(CustomUser)

        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            content_type=user_content_type, 
            object_id=user_to_follow.id 
        )
        
        return Response({'detail': f'Successfully followed {user_to_follow.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Unfollow a user.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all() 

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            
        request.user.following.remove(user_to_unfollow)

        return Response({'detail': f'Successfully unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)


# --- UPDATED USER VIEWSET ---

class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for listing and retrieving users.
    """
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer # FIX: Use CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]