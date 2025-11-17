"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from bookshelf.views import SignUpView  # RESTORED

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('relationship_app.urls')), # Remains commented out
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
                  TemplateView.as_view(template_name='accounts/profile.html'),
                  name='profile'),
    path("signup/", SignUpView.as_view(), name="signup"), # RESTORED
]