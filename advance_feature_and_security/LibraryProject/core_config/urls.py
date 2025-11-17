from django.contrib import admin
from django.urls import path, include
from core_security.views import security_home_view

urlpatterns = [
    # 1. Django Admin site
    path('admin/', admin.site.urls),

    # 2. TWO-FACTOR AUTHENTICATION (2FA) URLs - Using the string path to fix import conflict
    path('account/', include('two_factor.urls')),

    # 3. CORE APP URLs
    path('security/', security_home_view, name='security_home'),
]