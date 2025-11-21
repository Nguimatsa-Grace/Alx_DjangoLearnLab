"""
URL configuration for api_project project.
"""
from django.contrib import admin
from django.urls import path, include 
from api.views import api_root # <--- Make sure this line is included!

urlpatterns = [
    # Route the root path ('') to the simple view
    path('', api_root), 
    
    # The default Django Admin route
    path('admin/', admin.site.urls),
    
    # Route all requests starting with 'api/' to the 'api' app's urls.py
    path('api/', include('api.urls')),
]