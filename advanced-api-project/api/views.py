from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# --- 1. Author ViewSet (Remains unchanged) ---

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on the Author model.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# --- 2. Generic Views for the Book Model (Step 1, 3, 4) ---
# We use separate generic classes to control HTTP methods and permissions precisely. 

class BookList(generics.ListAPIView):
    """
    ListView: Retrieves a list of all books. (Read-only access)
    Permissions: Allows GET (read) to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Allows read access to anyone, but prevents forms/POST for unauthenticated users.
    permission_classes = [IsAuthenticatedOrReadOnly] 

class BookDetail(generics.RetrieveAPIView):
    """
    DetailView: Retrieves a single book instance. (Read-only access)
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
    # Step 4: Requires authentication to WRITE (POST).
    permission_classes = [IsAuthenticatedOrReadOnly] 

class BookUpdate(generics.UpdateAPIView):
    """
    UpdateView: Modifies an existing book instance (PUT/PATCH).
    Permissions: Restricts updates to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Requires authentication to WRITE (PUT/PATCH).
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDelete(generics.DestroyAPIView):
    """
    DeleteView: Deletes a book instance (DELETE).
    Permissions: Restricts deletion to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Step 4: Requires authentication to DELETE.
    permission_classes = [IsAuthenticatedOrReadOnly]