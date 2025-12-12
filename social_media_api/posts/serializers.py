# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import CustomUserSerializer # Assuming CustomUserSerializer is needed for nested Post data

# 1. PostSerializer (RESTORED/INCLUDED)
class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    
    # Assuming 'likes' is a ManyToMany field on the Post model
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'updated_at',
            'likes_count'
        )
        read_only_fields = ('author', 'created_at', 'updated_at', 'likes_count')
    
    def get_likes_count(self, obj):
        # Assuming your Post model has a related name 'post_likes' or similar 
        # that allows counting the likes. If you use a simple ManyToMany field named 'likes', 
        # use obj.likes.count()
        return obj.likes.count()


# 2. CommentSerializer (The one we fixed last time)
class CommentSerializer(serializers.ModelSerializer):
    # Assuming author serializer is needed here too
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 
            'content', 
            'post', # Kept as read-only or hidden field to be set in the view
            'author', 
            'created_at',
        )
        read_only_fields = (
            'id', 
            'post', # Should be read_only as it is set by the view kwargs
            'author', # Should be read_only as it is set by request.user
            'created_at',
        )
