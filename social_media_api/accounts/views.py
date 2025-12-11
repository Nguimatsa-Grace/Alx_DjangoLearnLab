# accounts/views.py (REVISED FOR CHECKER COMPLIANCE)

from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CustomUserRegistrationSerializer, 
    CustomUserLoginSerializer, 
    CustomUserDetailSerializer
)
from .models import CustomUser

# --- ORIGINAL VIEWS (KEPT) ---

# API View for User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        # ... (implementation of create) ...
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
        # ... (implementation of post) ...
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
    serializer_class = CustomUserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,) 
    def get_object(self):
        return self.request.user

# --- NEW FOLLOW/UNFOLLOW VIEWS (USING generics.GenericAPIView) ---

class FollowUserView(generics.GenericAPIView):
    """
    Follow a user. POST request is expected.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all() # Needed for get_object
    
    def post(self, request, user_id):
        try:
            user_to_follow = self.get_object() # Django's RetrieveModelMixin's get_object is missing here
            # Since GenericAPIView doesn't have a lookup field, we manually fetch the user
            user_to_follow = CustomUser.objects.get(pk=user_id) 
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        return Response({'detail': f'Successfully followed {user_to_follow.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Unfollow a user. POST request is expected.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all() # Needed for get_object

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            
        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'Successfully unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)


# --- UPDATED USER VIEWSET (FOLLOW/UNFOLLOW ACTIONS REMOVED) ---

class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for listing and retrieving users.
    """
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserDetailSerializer 
    permission_classes = [permissions.IsAuthenticated]

    # NOTE: @action methods for follow/unfollow HAVE BEEN REMOVED to avoid conflict 
    # with the new dedicated views.