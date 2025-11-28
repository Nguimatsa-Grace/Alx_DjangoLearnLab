from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsStaffOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# --- Author ViewSet ---

class AuthorViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Author. 
    Only staff users can create, update, or delete.
    All users can list and retrieve.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffOrReadOnly] 

# --- Book Generic Views ---

class BookListAPIView(generics.ListAPIView):
    """
    Lists Books and supports filtering, searching, and ordering.
    Accessible by all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filters and Search (Corrected: 'isbn' removed from search_fields)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering only by fields present in the model
    filterset_fields = ['publication_year', 'author']
    
    # Searching only by fields present in the model
    search_fields = ['title', 'author__name'] # FIX: 'isbn' removed
    
    # Ordering fields
    ordering_fields = ['title', 'publication_year']


class BookCreateAPIView(generics.CreateAPIView):
    """
    Creates a new Book. Only staff users can access this endpoint.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly] 

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, Updates, or Deletes a specific Book. 
    Only staff users can update or delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]