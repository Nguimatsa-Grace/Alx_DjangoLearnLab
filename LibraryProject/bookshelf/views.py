from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book # <-- Import the Book model

@login_required
def book_list(request):
    """
    Displays the list of all available books,
    and handles the logic for the dashboard view.
    """
    # 1. Fetch all books from the database
    books = Book.objects.all().order_by('title')
    
    # 2. Prepare the context to send to the template
    context = {
        'books': books
    }
    
    # 3. Render the template with the context
    return render(request, 'bookshelf/book_list.html', context)