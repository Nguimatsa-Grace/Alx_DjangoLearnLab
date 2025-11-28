from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsStaffOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# --- Author ViewSet ---

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsStaffOrReadOnly] 

# --- Book Generic Views ---

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filters and Search (from previous tasks)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'isbn']
    ordering_fields = ['title', 'publication_year']


class BookCreateAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly] 

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]