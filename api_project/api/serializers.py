from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Book model instances to JSON format.
    It includes all fields: id (automatically added by Django), title, and author.
    """
    class Meta:
        model = Book
        fields = '__all__' # Includes 'id', 'title', and 'author'