from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth import get_user_model

# Import serializers
from .serializers import (
    UserRegistrationSerializer,
    CustomUserLoginSerializer,
    CustomUserSerializer
)

# FIXED: Import from 'notifications', not 'social_notifications'
from notifications.models import Notification

User = get_user_model()

# API View for User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Ensure a token is created for the new user
        token, created = Token.objects.get_or_create(user=user) 
        response_data = serializer.data
        response_data['token'] = token.key
        return Response(response_data, status=status.HTTP_201_CREATED)

# API View for User Login and Token Retrieval
class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
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
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,) 

    def get_object(self):
        return self.request.user

# --- FOLLOW/UNFOLLOW VIEWS ---

class FollowUserView(generics.GenericAPIView):
    """
    Follow a user and creates a notification for the recipient.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all() 
    
    def post(self, request, user_id):
        user_to_follow = generics.get_object_or_404(User, pk=user_id)

        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)

        # CREATE FOLLOW NOTIFICATION
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            target=user_to_follow,
            content_type=ContentType.objects.get_for_model(User),
            object_id=user_to_follow.id 
        )
        
        return Response({'detail': f'Successfully followed {user_to_follow.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Unfollow a user.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all() 

    def post(self, request, user_id):
        user_to_unfollow = generics.get_object_or_404(User, pk=user_id)

        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            
        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'Successfully unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for listing and retrieving users.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]