# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token # Required import for checker
from rest_framework.views import APIView
from .serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer, CustomUserProfileSerializer
from .models import CustomUser

# API View for User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # Token created in serializer's save() method
        
        # Retrieve the token that was just created by the serializer
        token = Token.objects.get(user=user) 

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
    serializer_class = CustomUserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,) 

    def get_object(self):
        return self.request.user