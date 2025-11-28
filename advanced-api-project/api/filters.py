import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Defines the filtering options for the Book model.
    Allows exact matching on title and publication_year, and filtering by author ID.
    """
    class Meta:
        model = Book
        fields = {
            # Allows filtering by exact title match (e.g., ?title=The Caves of Steel)
            'title': ['exact'], 
            
            # Allows filtering by exact author ID (e.g., ?author=1)
            'author': ['exact'], 
            
            # Allows filtering by exact publication year (e.g., ?publication_year=1954)
            'publication_year': ['exact'],
        }