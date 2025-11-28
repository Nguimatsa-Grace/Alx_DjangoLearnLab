from django.urls import path, include
from rest_framework import routers
from . import views

# Router for ViewSets (Author)
router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')

urlpatterns = [
    # Router URLs for AuthorViewSet (generates author-list, author-detail)
    path('', include(router.urls)),

    # Explicit URLs for Book views to match the test naming convention exactly
    # List (GET) and Filtering/Ordering
    path('books/', views.BookListAPIView.as_view(), name='book-list'), 
    
    # Create (POST)
    path('books/create/', views.BookCreateAPIView.as_view(), name='book-create'), 
    
    # Detail (GET, PUT, DELETE)
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
]