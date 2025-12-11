# social_media_api/urls.py (Corrected)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # User Authentication Endpoints (djoser)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # API Endpoints for Posts and Comments (This line should resolve the error)
    path('', include('posts.urls')), 
]