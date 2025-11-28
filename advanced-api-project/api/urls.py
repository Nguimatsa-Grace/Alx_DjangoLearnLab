from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# Note: The AuthorViewSet is handled by the router in the project's urls.py.

urlpatterns = [
    # Book Generic Views (Task 1 Endpoints)
    # List (GET)
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Detail (GET)
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    
    # Create (POST)
    path('books/create/', views.BookCreate.as_view(), name='book-create'),
    
    # Update (PUT/PATCH)
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    
    # Delete (DELETE)
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)