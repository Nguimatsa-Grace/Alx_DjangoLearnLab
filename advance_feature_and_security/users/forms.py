from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser objects.
    Ensures that the new custom fields are included in the creation form.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Fields restored to include custom fields
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'profile_photo', 'email',)

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing CustomUser objects.
    Ensures that the new custom fields are editable in the admin.
    """
    class Meta:
        model = CustomUser
        # Fields restored to include custom fields
        fields = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')