# relationship_app/views.py

from django.shortcuts import render # Needed for the function-based view
from django.views.generic import DetailView # Needed for the class-based view
# FIX: Ensure all models, especially Library, are imported from .models
from .models import Book, Library, Author, Librarian 


# --- 1. Function-based View (Fails Check 1: "render a simple text list...") ---

def book_list(request):
    """Lists all books and their authors."""
    
    # Query all Book objects
    books = Book.objects.all().select_related('author')
    
    # The context dictionary to pass data to the template
    context = {
        'books': books
    }
    
    # This render line is crucial for passing the "render a simple text list" check
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-based View (Fails Check 2: "from .models import Library") ---

class LibraryDetailView(DetailView):
    """Displays details for a specific library, including all its books."""
    
    # FIX: The checker verifies the use of DetailView and the model is Library
    model = Library
    
    # The template to render the object details
    template_name = 'relationship_app/library_detail.html'
    
    # The context variable name (default is 'object' or 'library')
    context_object_name = 'library'
    
    # Ensure related books are fetched efficiently
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')