from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Django Admin Panel URL
    path('admin/', admin.site.urls),
    
    # 2. Access Control URLs (This handles the root path and authentication)
    # The login page for the whole project should be here.
    path('', include('access_control.urls')),
    
    # 3. Bookshelf App URLs
    path('bookshelf/', include('bookshelf.urls')),
]