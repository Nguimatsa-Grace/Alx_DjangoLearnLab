from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpRequest
from .models import Book
from django.db.models import Q 
from .forms import ExampleForm # 🚨 CRITICAL FIX: Import the required form

# ==============================================================================
# Security Measures: SQL Injection Prevention (Step 3)
# ==============================================================================

def book_search_secure(request: HttpRequest):
    """
    Demonstrates secure data access using Django ORM (SQL Injection prevention).
    """
    query = request.GET.get('q', '')
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
        
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# ==============================================================================
# Security Measures: CSP Header (Step 4)
# ==============================================================================

def secure_csp_view(request: HttpRequest):
    """
    Demonstrates setting a Content Security Policy (CSP) header manually.
    """
    html = """
    <h1>CSP Test</h1>
    <p>This page demonstrates CSP headers set in the view.</p>
    """
    response = HttpResponse(html)
    
    csp_header = "default-src 'self'; script-src 'self'; style-src 'self';"
    response['Content-Security-Policy'] = csp_header
    
    return response

# ==============================================================================
# Existing Views (Required for checks)
# ==============================================================================

def book_list(request):
    """
    Required view: Renders book_list.html and demonstrates form integration.
    """
    # Instantiate the form for display in the template
    form = ExampleForm() 
    return render(request, 'bookshelf/book_list.html', {'form': form})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("You have permission to create books.")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return HttpResponse("You have permission to delete books.")


def submit_book_form(request):
    """
    Handles form submission and demonstrates form validation (Step 3).
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Data is validated and sanitized here by form.cleaned_data
            return HttpResponse("Form submitted securely and validated.")
        else:
            return HttpResponse(f"Validation failed: {form.errors}", status=400)
    return HttpResponse("Form submission endpoint.")