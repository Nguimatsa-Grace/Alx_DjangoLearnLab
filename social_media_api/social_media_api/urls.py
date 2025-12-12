from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This links your project to the accounts app
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),
]