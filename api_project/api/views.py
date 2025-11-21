from django.http import HttpResponse
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# This is the temporary view for the project root (from Task 0 fix)
def api_root(request):
    return HttpResponse("<h1>API Project Setup Successful!</h1><p>Navigate to /admin/ or /api/ for development.</p>")

# Task 1: API View to list all books
class BookList(generics.ListAPIView):
    """
    A view that uses ModelSerializer and ListAPIView to fetch and list all Book objects.
    
    - queryset: Defines the data source (all Book objects).
    - serializer_class: Specifies how to convert the data into JSON/API format.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer