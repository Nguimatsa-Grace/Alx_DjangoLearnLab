# relationship_app/views.py (Restored Full Version for Task 3)

from django.shortcuts import render, redirect 
from django.views.generic.detail import DetailView 
from django.contrib.auth.decorators import login_required, user_passes_test # <-- RESTORED: For RBAC views

# --- Imports required by Checkers (including explicit ones) ---
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from .models import Book, Library, Author, Librarian, UserProfile # <-- RESTORED: UserProfile added
from .forms import CustomUserCreationForm # <-- RESTORED
from django.contrib.auth import views as auth_views 


# --- 1. Function-based View (List Books) ---

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


# --- 2. Class-based View (Library Detail) ---

class LibraryDetailView(DetailView):
    """Displays details for a specific library, including all its books."""
    
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')


# --- 3. Registration View (RESTORED logic) ---

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'relationship_app/register.html', {'form': form})


# --- RBAC Helper Functions (RESTORED for Task 3) ---

def is_admin(user):
    """Checks if the user has the 'Admin' role."""
    # Ensure user is logged in, has a profile, and the role is 'Admin'
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Checks if the user has the 'Librarian' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Checks if the user has the 'Member' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# --- Role-Based Views (RESTORED for Task 3) ---

@login_required
@user_passes_test(is_admin, login_url='/login/') 
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@login_required
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@login_required
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """View accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})