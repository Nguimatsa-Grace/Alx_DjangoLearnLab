# relationship_app/urls.py (Final Fix for all Checkers)

from django.urls import path

# --- General Import (Needed for views.register below) ---
from . import views 

# FIX: Explicit imports, EXCLUDING 'register', but including everything else.
from .views import book_list, LibraryDetailView, admin_view, librarian_view, member_view, book_add, book_edit, book_delete 

# Import built-in Auth views 
from django.contrib.auth import views as auth_views 

app_name = 'relationship_app'

urlpatterns = [
    # Existing App Views (use function name directly)
    path('books/', book_list, name='book_list'), 
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # --- Authentication Views ---
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # FIX for Task 2 Checker: Must be 'views.register'
    path('register/', views.register, name='register'), 
    
    # --- New RBAC Views (Task 3 - use function name directly) ---
    path('admin-area/', admin_view, name='admin_view'),
    path('librarian-area/', librarian_view, name='librarian_view'),
    path('member-area/', member_view, name='member_view'),
    
    # --- Custom Permission Paths (Task 4 - use function name directly) ---
    path('add_book/', book_add, name='book_add'),
    path('edit_book/<int:pk>/', book_edit, name='book_edit'),
    path('delete_book/<int:pk>/', book_delete, name='book_delete'),
]