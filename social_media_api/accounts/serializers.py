# accounts/serializers.py (CLEAN, CONSOLIDATED)

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token 
from .models import CustomUser

# Serializer for User Registration
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user

# Serializer for User Login
class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials.")

# Serializer for User Profile/Detail (Consolidated name used for all detail views)
class CustomUserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField() # To check if current user follows this user
    
    class Meta:
        model = CustomUser
        # Removed 'bio' and other fields that may not exist in your model
        fields = ('id', 'username', 'email', 'profile_picture', 'date_joined', 'followers_count', 'following_count', 'is_following')
        read_only_fields = ('username', 'email', 'date_joined')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_is_following(self, obj):
        # Checks if the user making the request is following 'obj'
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(pk=obj.pk).exists()
        return False