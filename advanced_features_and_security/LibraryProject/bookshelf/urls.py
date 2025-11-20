from django.urls import path
from . import views

urlpatterns = [
    # Required list view
    path('books/', views.book_list, name='book_list'),
    
    # Map the custom permission-required views
    path('create/', views.create_book, name='create_book'),
    path('delete/', views.delete_book, name='delete_book'),
]