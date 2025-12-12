from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from notifications.models import Notification 

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials.")

class NotificationSerializer(serializers.ModelSerializer):
    actor = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)
    target = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'recipient', 'verb', 'target', 'created_at', 'is_read']