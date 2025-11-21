from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet 

# Create a router instance
router = DefaultRouter()

# Register the BookViewSet with the router. 
# This handles all CRUD operations under the 'books_all' prefix.
router.register(r'books_all', BookViewSet, basename='book_all')

# Combine the specific 'books/' path and the router paths
urlpatterns = [
    # Route for the BookList view (Task 1 compatibility)
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
]