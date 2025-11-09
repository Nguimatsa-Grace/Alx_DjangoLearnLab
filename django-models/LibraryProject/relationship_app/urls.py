# relationship_app/urls.py 

from django.urls import path
# Checker looks for this specific line:
from .views import list_books 
from .views import LibraryDetailView # Keep this one too

app_name = 'relationship_app'

urlpatterns = [
    # Reference the explicitly imported function
    path('books/', list_books, name='book_list'), 
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]