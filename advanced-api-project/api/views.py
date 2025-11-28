from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsStaffOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

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

# Combining List and Create into one view to consolidate permissions and settings
class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles listing of Books (accessible to all) and creation of Books (staff only).
    Explicitly disables pagination to ensure tests expecting an array pass.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permissions are split by HTTP method:
    # GET/HEAD/OPTIONS (list) are IsAuthenticatedOrReadOnly (i.e., read allowed)
    # POST (create) is IsStaffOrReadOnly (i.e., create only allowed for staff)
    permission_classes = [IsStaffOrReadOnly] 

    # Explicitly set pagination_class to None to guarantee the response is a list/array,
    # which is required for the tests to pass.
    pagination_class = None

    # Filters and Search 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'author__name'] 
    ordering_fields = ['title', 'publication_year']


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, Updates, or Deletes a specific Book. 
    Only staff users can update or delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]