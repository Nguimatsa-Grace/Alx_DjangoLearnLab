from django.urls import path
from .views import BookList

urlpatterns = [
    # Task 1 Endpoint: Maps /api/books/ to the BookList view
    path('books/', BookList.as_view(), name='book-list'), 
]