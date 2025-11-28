from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Author instances.
    It uses the AuthorSerializer, which includes the nested Book data 
    for retrieval (GET requests).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Book instances.
    It uses the BookSerializer, which enforces the custom validation 
    on the publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer