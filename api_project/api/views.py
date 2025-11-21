from django.http import HttpResponse
from rest_framework import viewsets, generics 
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from .models import Book
from .serializers import BookSerializer

# Temporary view for the project root (from Task 0 fix)
def api_root(request):
    return HttpResponse("<h1>API Project Setup Successful!</h1><p>Navigate to /admin/ or /api/ for development.</p>")

# Task 1 List View (Kept for compatibility with the old '/api/books/' URL)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
# Task 3: New View for books with 'Dune' in the title
class DuneBookList(generics.ListAPIView):
    """
    Exposes only books with the title 'Dune' using the custom manager method.
    """
    queryset = Book.objects.get_dune_books() # Use the custom manager method
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Require authentication to access this special list

# Task 2/3: ViewSet for all CRUD operations, now with permissions
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD operations (List, Retrieve, Create, Update, Destroy) 
    for the Book model using ModelViewSet.
    
    Permissions: Requires authentication for all operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # 🚨 Task 3 Addition: Require users to be authenticated to perform any action
    permission_classes = [IsAuthenticated]