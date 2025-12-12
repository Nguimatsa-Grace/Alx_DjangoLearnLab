from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from social_notifications.models import Notification  # Corrected import

User = get_user_model()

# 1. Serializer for User Display (used in many places)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', 'username', 'email')

# 2. Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Ensure password is write only for security
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        # Using create_user ensures the password is properly hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# 3. Serializer for User Login
class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data

# 4. Serializer for Notifications (Crucial for Task 3)
class NotificationSerializer(serializers.ModelSerializer):
    actor = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)
    # Target is a GenericForeignKey, so we represent it as a string or ID
    target = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'recipient', 'verb', 'target', 'created_at', 'is_read']