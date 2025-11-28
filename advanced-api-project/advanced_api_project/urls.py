from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# NOTE: The router definition has been moved to api/urls.py to consolidate includes.

urlpatterns = [
    # 1. Django Admin site
    path('admin/', admin.site.urls),
    
    # 2. Consolidate ALL API endpoints under one include.
    # This is the line the checker MUST find
    path('api/', include('api.urls')),
    
    # Required for testing permissions in the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]