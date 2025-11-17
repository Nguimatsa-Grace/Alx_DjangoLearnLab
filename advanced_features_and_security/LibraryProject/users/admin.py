from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Defines the admin interface for the CustomUser model.
    """
    # Fields to display in the list view
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth', # New field
        'is_staff'
    )
    
    # Fields to be searched
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Configuration for the user change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 
            'last_name', 
            'date_of_birth', # New field
            'profile_photo' # New field
        )}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Configuration for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password', 
                'password2', 
                'first_name', 
                'last_name', 
                'date_of_birth', # New field
                'profile_photo' # New field
            ),
        }),
    )
    
    # Ensure 'password2' field is available for the add_fieldsets
    add_form_fields = list(add_fieldsets[0][1]['fields'])
    add_form_fields.insert(add_form_fields.index('password') + 1, 'password2')
    add_fieldsets[0][1]['fields'] = tuple(add_form_fields)
    

admin.site.register(CustomUser, CustomUserAdmin)