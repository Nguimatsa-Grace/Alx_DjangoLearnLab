from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Specify the model being managed
    model = CustomUser
    
    # Fields displayed in the list view (table of users)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

    # Redefine the fieldsets for the change user form to include custom fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'profile_photo',
            'username', 
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define the fields shown on the Add User form 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )
    
    ordering = ('email',)

# Register the model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)