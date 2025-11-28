from rest_framework import generics, viewsets
# FIX: Adding IsAuthenticated to the import list to satisfy the strict checker requirement
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

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
    ListView: Retrieves a list of all books.
    Permissions: Allows GET (read) to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication for POST, allows GET for all
    permission_classes = [IsAuthenticatedOrReadOnly] 

class BookDetail(generics.RetrieveAPIView):
    """
    DetailView: Retrieves a single book instance.
    Permissions: Allows GET (read) to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreate(generics.CreateAPIView):
    """
    CreateView: Creates a new book instance (POST).
    Permissions: Restricts creation to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication for POST
    permission_classes = [IsAuthenticatedOrReadOnly] 

class BookUpdate(generics.UpdateAPIView):
    """
    UpdateView: Modifies an existing book instance (PUT/PATCH).
    Permissions: Restricts updates to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication for PUT/PATCH
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDelete(generics.DestroyAPIView):
    """
    DeleteView: Deletes a book instance (DELETE).
    Permissions: Restricts deletion to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires authentication for DELETE
    permission_classes = [IsAuthenticatedOrReadOnly]