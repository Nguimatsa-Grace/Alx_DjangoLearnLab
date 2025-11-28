from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# --- Author ViewSet (Standard DRF Router) ---

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Author instances. 
    Uses IsStaffOrReadOnly permission class.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffOrReadOnly]
    
# --- Book Generic Views ---

class BookListAPIView(generics.ListAPIView):
    """
    List all books, supporting filtering, searching, and ordering.
    Read-only for all users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Allow all to read

    # Filters and Search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'isbn']
    ordering_fields = ['title', 'publication_year']


class BookCreateAPIView(generics.CreateAPIView):
    """
    Create a new book instance. Restricted to staff users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly] # Only staff can create

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a book instance.
    Retrieve is allowed for all, Update/Delete restricted to staff users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly] # Only staff can update/delete