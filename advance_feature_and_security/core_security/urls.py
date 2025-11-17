from django.contrib import admin
from django.urls import path, include
# CRITICAL FIX: Import the URLs directly to bypass Django's string lookup issues
from two_factor import urls as two_factor_urls 
from core_security.views import security_home_view 

urlpatterns = [
    # 1. Django Admin site
    path('admin/', admin.site.urls),

    # 2. TWO-FACTOR AUTHENTICATION (2FA) URLS
    # We pass the imported module object (two_factor_urls), NOT a string 'two_factor.urls'
    path('account/', include(two_factor_urls)),
    
    # 3. CORE APP URLS
    path('security/', security_home_view, name='security_home'),
]