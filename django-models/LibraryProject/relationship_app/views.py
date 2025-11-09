# relationship_app/views.py

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library, Author, Librarian
from django.http import HttpResponse # Added for simple text output reference

# --- 1. Function-based View (for all books) ---

def book_list(request):
    """Lists all books and their authors."""
    
    # Query all Book objects
    books = Book.objects.all().select_related('author')
    
    # The context dictionary to pass data to the template
    context = {
        'books': books
    }
    
    # Renders the template 'relationship_app/list_books.html'
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-based View (for single library details) ---

class LibraryDetailView(DetailView):
    """Displays details for a specific library, including all its books."""
    
    # The model this view operates on
    model = Library
    
    # The template to render the object details (will be relationship_app/library_detail.html)
    template_name = 'relationship_app/library_detail.html'
    
    # The context variable name to use in the template (default is 'object' or 'library')
    context_object_name = 'library'
    
    # Ensure related books are fetched efficiently
    def get_queryset(self):
        # Prefetch the books and their authors to avoid multiple database hits
        return Library.objects.prefetch_related('books__author')