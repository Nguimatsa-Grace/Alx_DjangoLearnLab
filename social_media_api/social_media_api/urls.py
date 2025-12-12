from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # User Authentication Endpoints (djoser)
    # Note: Ensure djoser is in your INSTALLED_APPS in settings.py
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # API Endpoints for Follows and Users (accessible at /api/users/)
    path('api/', include('accounts.urls')), 

    # API Endpoints for Posts and Comments
    path('api/', include('posts.urls')), 
    
    # --- FIXED NOTIFICATIONS ROUTE ---
    # Points to 'social_notifications' which is the app registered in settings
    path('notifications/', include('social_notifications.urls')),
]