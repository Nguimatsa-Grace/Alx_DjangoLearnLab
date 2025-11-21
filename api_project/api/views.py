from django.http import HttpResponse
from rest_framework import viewsets, generics 
from .models import Book
from .serializers import BookSerializer

# Temporary view for the project root (from Task 0 fix)
def api_root(request):
    return HttpResponse("<h1>API Project Setup Successful!</h1><p>Navigate to /admin/ or /api/ for development.</p>")

# Task 1 List View (Kept for compatibility with the old '/api/books/' URL)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Task 2: ViewSet for all CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD operations (List, Retrieve, Create, Update, Destroy) 
    for the Book model using ModelViewSet.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer