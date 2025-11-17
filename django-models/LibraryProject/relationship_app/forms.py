# relationship_app/forms.py
from django.contrib.auth.forms import UserCreationForm

# We inherit from Django's built-in UserCreationForm for a standard registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Use the default User model
        fields = UserCreationForm.Meta.fields + ("email",) 
        # Note: You can add more fields if needed, but 'email' is a common addition