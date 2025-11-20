from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as two_factor_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView # <--- NEW IMPORT

# NOTE: This file is intentionally renamed from urls.py to project_urls_fixed.py
# The settings.py file is configured to look here via ROOT_URLCONF = 'config.project_urls_fixed'

# CRITICAL FIX: To avoid the redirect loop, we must explicitly use the 
# standard login view for the admin site, bypassing the two_factor patch.
admin.site.login = admin.site.uncached_url(admin.site.login_view)

urlpatterns = [
    # TEMPORARILY COMMENT OUT 2FA URLs to avoid dependency error
    # path('', include(two_factor_urls)),

    # User URLs (Assuming the main user login/logout paths start here)
    path('account/', include('users.urls')),
    
    path('admin/', admin.site.urls),
    path('library/', include('bookshelf.urls')), 
    
    # NEW FIX: Redirect the root path (/) directly to the Admin login
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)), 

    # COMMENTED OUT the unused relationship_app
    # path('relationship/', include('relationship_app.urls')), 
]

# Configure URL patterns for serving media files (like profile pictures)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)