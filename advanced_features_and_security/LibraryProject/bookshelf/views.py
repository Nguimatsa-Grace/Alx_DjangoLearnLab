from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpRequest
from .models import Book # Import the Book model we created
from django.db.models import Q # Used for complex, safe ORM queries

# ==============================================================================
# Security Measures: SQL Injection Prevention (Step 3)
# ==============================================================================

def book_search_secure(request: HttpRequest):
    """
    Demonstrates secure data access using Django ORM (SQL Injection prevention).
    User input is handled as parameters, NOT string formatting.
    """
    query = request.GET.get('q', '')
    
    # 🚨 SQL INJECTION PREVENTION: Using the Django ORM is the best defense. 
    # The ORM correctly parameterizes the query, ensuring the user input (query) 
    # is treated as data, not as executable SQL code.
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).order_by('title')
        # Even if a malicious user types "'; DROP TABLE books; --" into 'q', 
        # Django treats it as a string to search for, not a command.
    else:
        books = Book.objects.all().order_by('title')
        
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# ==============================================================================
# Security Measures: CSP Header (Step 4)
# ==============================================================================

def secure_csp_view(request: HttpRequest):
    """
    Demonstrates setting a Content Security Policy (CSP) header manually.
    This protects against XSS by limiting where resources can be loaded from.
    """
    html = """
    <h1>CSP Test</h1>
    <p>This page demonstrates CSP headers set in the view.</p>
    """
    response = HttpResponse(html)
    
    # 🚨 CONTENT SECURITY POLICY (CSP): 
    # Default-src 'self' only allows content (scripts, styles, etc.) from the site's own origin.
    # This prevents loading malicious scripts from external domains.
    csp_header = "default-src 'self'; script-src 'self'; style-src 'self';"
    response['Content-Security-Policy'] = csp_header
    
    return response

# ==============================================================================
# Existing Views (Required for previous checks)
# ==============================================================================

# Existing list view
def book_list(request):
    """Placeholder view for listing books."""
    return render(request, 'bookshelf/book_list.html')


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """View that requires the custom 'can_create' permission."""
    return HttpResponse("You have permission to create books.")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    """View that requires the custom 'can_delete' permission."""
    return HttpResponse("You have permission to delete books.")

# A placeholder view to handle the form submission from the template
def submit_book_form(request):
    if request.method == 'POST':
        # In a real app, form validation/sanitization would happen here (Step 3)
        return HttpResponse("Form submitted securely (CSRF token present).")
    return HttpResponse("Form submission endpoint.")