# relationship_app/urls.py (Fix for final Import Error)

from django.urls import path
from . import views # <-- Keep this general import!

# Delete or comment out the line below to fix the ImportError during migration
# from .views import list_books, LibraryDetailView 

# Import built-in Auth views (needed for Task 2)
from django.contrib.auth import views as auth_views 

app_name = 'relationship_app'

urlpatterns = [
    # Existing App Views
    # FIX: Use the generic views.list_books style
    path('books/', views.book_list, name='book_list'), 
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # --- Authentication Views ---
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # --- New RBAC Views (Task 3) ---
    path('admin-area/', views.admin_view, name='admin_view'),
    path('librarian-area/', views.librarian_view, name='librarian_view'),
    path('member-area/', views.member_view, name='member_view'),
]