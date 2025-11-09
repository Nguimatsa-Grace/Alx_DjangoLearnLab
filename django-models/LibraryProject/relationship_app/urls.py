# relationship_app/urls.py (Updated with Auth URLs)

from django.urls import path
from .views import list_books, register # Added 'register'
from .views import LibraryDetailView
# Import built-in Auth views
from django.contrib.auth import views as auth_views 

app_name = 'relationship_app'

urlpatterns = [
    # Existing App Views
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # --- New Authentication Views ---
    
    # 1. Login View (Uses Django's built-in LoginView)
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # 2. Logout View (Uses Django's built-in LogoutView)
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # 3. Registration View (Uses your custom function)
    path('register/', register, name='register'),
]