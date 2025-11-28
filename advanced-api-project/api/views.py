from rest_framework import generics, viewsets
# Import necessary filter/search/ordering backends
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter # Import the custom filterset


# --- 1. Author ViewSet (Remains unchanged) ---

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on the Author model.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# --- 2. Generic Views for the Book Model ---

class BookList(generics.ListAPIView):
    """
    ListView: Retrieves a list of all books, now with filtering, searching, and ordering.
    Permissions: Allows GET (read) to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    # TASK 2 ADDITIONS: Filtering, Searching, and Ordering
    # Step 1: Filtering by specific fields using the custom filter class
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter

    # Step 2: Search functionality on title and author (uses __str__ of author)
    search_fields = ['title', 'author__name'] # Search on book title and the author's name field
    
    # Step 3: Ordering by fields
    ordering_fields = ['title', 'publication_year', 'author']
    # Optional: set a default ordering
    ordering = ['title'] 


class BookDetail(generics.RetrieveAPIView):
    """
    DetailView: Retrieves a single book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreate(generics.CreateAPIView):
    """
    CreateView: Creates a new book instance (POST).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

class BookUpdate(generics.UpdateAPIView):
    """
    UpdateView: Modifies an existing book instance (PUT/PATCH).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDelete(generics.DestroyAPIView):
    """
    DeleteView: Deletes a book instance (DELETE).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]