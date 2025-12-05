# File: blog/urls.py

from django.urls import path
from . import views
# Import built-in views for login/logout
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # Q0: Home page URL
    path('', views.post_list, name='post_list'),
    
    # Q1: Authentication URLs
    
    # 1. Registration
    path('register/', views.register, name='register'),
    
    # 2. Login (Uses Django's built-in view)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    
    # 3. Logout (Uses Django's built-in view)
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # 4. Profile Management
    path('profile/', views.profile, name='profile'),
]