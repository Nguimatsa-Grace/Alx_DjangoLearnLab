import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

# Create a default router for ViewSets
router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the router URLs for AuthorViewSet (generates author-list, author-detail)
    path('api/', include(router.urls)),

    # Explicit URLs for Book views to match the test naming convention exactly
    # 1. BookListAPIView (GET for list, uses book-list name for filtering/ordering tests)
    path('api/books/', views.BookListAPIView.as_view(), name='book-list'), 
    
    # 2. BookCreateAPIView (POST for creation, uses book-create name for creation test)
    path('api/books/create/', views.BookCreateAPIView.as_view(), name='book-create'), 
    
    # 3. BookDetailAPIView (GET, PUT, DELETE, uses book-detail name for all detail operations)
    path('api/books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
]