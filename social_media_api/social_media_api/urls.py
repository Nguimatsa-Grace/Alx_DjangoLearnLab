from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Essential for Task 0 & 1 checker
    path('api/accounts/', include('accounts.urls')),
    
    # Essential for Task 2 (Feed) and Task 3 (Likes)
    path('api/posts/', include('posts.urls')),
]