# File: django_blog/django_blog/urls.py
from django.contrib import admin
from django.urls import path, include # <-- Make sure 'include' is here!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myblog.urls')),
]