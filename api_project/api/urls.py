from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token # 🚨 Task 3 Import
from .views import BookList, BookViewSet, DuneBookList # 🚨 Task 3 Import

# Create a router instance
router = DefaultRouter()

# Register the BookViewSet with the router. 
# This handles all CRUD operations under the 'books_all' prefix.
router.register(r'books_all', BookViewSet, basename='book_all')

# Combine the specific 'books/' path and the router paths
urlpatterns = [
    # Route for the BookList view (Task 1 compatibility)
    path('books/', BookList.as_view(), name='book-list'),
    
    # 🚨 Task 3: Token Authentication Endpoint
    path('auth/get-token/', obtain_auth_token, name='get_token'),

    # 🚨 Task 3: New Custom Manager Endpoint
    path('dune-books/', DuneBookList.as_view(), name='dune-books'),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
]