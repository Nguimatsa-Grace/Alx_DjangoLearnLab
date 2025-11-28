from rest_framework import serializers
# --- CORRECT IMPORT: Importing models, NOT serializers ---
from .models import Author, Book 
from django.utils import timezone

# Step 4: Create Custom Serializers

# --- 1. Book Serializer with Custom Validation ---

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    This serializer handles creating and updating Book instances.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validator that checks if the input publication year (value) 
        is greater than the current year.
        """
        current_year = timezone.now().year
        if value > current_year:
            # Raises a 400 Bad Request if the year is in the future.
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

# --- 2. Author Serializer with Nested Relationship ---

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    
    This serializer includes nested book data, making the Author's full information 
    (including their published books) available in one request.
    """
    # Nested field: It correctly references BookSerializer, which is defined earlier in this file.
    books = BookSerializer(many=True, read_only=True) 

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']