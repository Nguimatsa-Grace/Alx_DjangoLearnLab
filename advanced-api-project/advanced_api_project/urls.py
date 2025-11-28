from django.contrib import admin
from django.urls import path, include
from rest_framework import routers # Keep router import for backward compatibility if needed, but the project now uses Generic Views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Task 1 Requirement: Ensure the API URLs are included here
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]