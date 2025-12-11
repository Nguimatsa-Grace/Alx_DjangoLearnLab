from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# --- Utility Serializer for User Details ---
# Use this to show post/comment author details without exposing sensitive info
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'profile_picture') # Assuming profile_picture field exists

# --- Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('post',) # Post FK will be handled by the view

# --- Post Serializer ---
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        read_only_fields = ('created_at', 'updated_at')

    def get_comment_count(self, obj):
        # Optimized way to get the comment count
        return obj.comments.count()