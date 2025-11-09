# relationship_app/urls.py (Updated)

from django.urls import path
from . import views
from .views import LibraryDetailView # Import the Class-based View

app_name = 'relationship_app'

urlpatterns = [
    # 1. Function-based View URL (e.g., /books/)
    path('books/', views.book_list, name='book_list'),
    
    # 2. Class-based View URL (e.g., /library/1/)
    # The <int:pk> captures a number (the Primary Key) from the URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]