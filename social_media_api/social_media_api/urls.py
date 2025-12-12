# social_media_api/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # User Authentication Endpoints (djoser)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # API Endpoints for Follows and Users (accessible at /api/users/)
    path('api/', include('accounts.urls')), 

    # API Endpoints for Posts and Comments (accessible at /posts/, etc.)
    path('', include('posts.urls')), 
    # NEW API URL FOR NOTIFICATIONS
    path('notifications/', include('notifications.urls')),
]