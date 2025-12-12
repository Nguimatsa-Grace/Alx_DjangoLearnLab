# accounts/serializers.py (ABSOLUTE FINAL VERSION - ALL SERIALIZERS)

from rest_framework import serializers
from django.contrib.auth import authenticate 
from .models import CustomUser

# Serializer for display (used by NotificationSerializer)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', 'username', 'email')

# Serializer for User Login (This is the missing one)
class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # NOTE: Using authenticate() is correct for token login
        user = authenticate(username=data.get('username'), password=data.get('password'))
        
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials.")


# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user