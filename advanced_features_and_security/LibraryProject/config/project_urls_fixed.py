from django.contrib import admin
from django.urls import path, include
# The two-factor import has been REMOVED
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# NOTE: This file is intentionally renamed from urls.py to project_urls_fixed.py

# The admin override line (admin.site.login = ...) has been REMOVED

urlpatterns = [
    # User URLs (Assuming the main user login/logout paths start here)
    path('account/', include('users.urls')),
    
    path('admin/', admin.site.urls),
    path('library/', include('bookshelf.urls')), 
    
    # FIX: Redirect the root path (/) directly to the Admin login
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)), 

    # COMMENTED OUT the unused relationship_app
    # path('relationship/', include('relationship_app.urls')), 
]

# Configure URL patterns for serving media files (like profile pictures)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)