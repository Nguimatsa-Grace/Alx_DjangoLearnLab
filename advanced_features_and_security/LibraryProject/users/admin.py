# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AlreadyRegistered
from .models import CustomUser 
# Make sure your CustomUser model is correctly imported from .models

# Define the CustomUserAdmin class (Use your existing fields/logic here)
class CustomUserAdmin(UserAdmin):
    # Add any custom fieldsets, list_display, list_filter, etc. here
    # Example:
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('custom_field',)}),
    # )
    pass

# --- CRITICAL FIX START ---
# Wrap the registration in a try/except block to prevent the AlreadyRegistered error.
try:
    admin.site.register(CustomUser, CustomUserAdmin)
except AlreadyRegistered:
    # This ensures that if the model was already registered (e.g., via 
    # an internal import or another configuration), we don't crash the server.
    pass
# --- CRITICAL FIX END ---

# Register other models in the users app here if needed