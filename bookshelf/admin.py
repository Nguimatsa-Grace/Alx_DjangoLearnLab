from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # This uses the default fields plus the custom ones
    list_display = UserAdmin.list_display + ('date_of_birth', 'profile_photo',)
    
    # Add custom fields to the detail page fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)