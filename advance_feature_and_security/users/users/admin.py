from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Customizes the Django Admin interface for the CustomUser model.
    It integrates our custom creation and change forms.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Custom fields to display in the user list view
    list_display = ['email', 'username', 'age', 'is_staff']
    
    # Custom fields to display in the detailed user change view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )
    # Custom fields to display in the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age',)}),
    )