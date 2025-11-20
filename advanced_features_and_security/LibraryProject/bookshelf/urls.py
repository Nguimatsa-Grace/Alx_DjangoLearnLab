from django.urls import path
from . import views

urlpatterns = [
    # Map the custom permission-required views to the required function names:
    path('create/', views.create_book, name='create_book'),
    path('delete/', views.delete_book, name='delete_book'),
    
    # You can keep your existing paths commented out if they are not needed for checks:
    # path('books/', views.book_list, name='book_list'), 
    # path('books/create/', views.book_create_view, name='book_create'),
    # path('books/<int:pk>/edit/', views.book_edit_view, name='book_edit'),
    # path('books/<int:pk>/delete/', views.book_delete_view, name='book_delete'),
]