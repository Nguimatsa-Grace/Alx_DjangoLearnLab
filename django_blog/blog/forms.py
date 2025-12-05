# File: blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Custom form for user registration
class CustomUserCreationForm(UserCreationForm):
    # The default UserCreationForm only includes username and password.
    # We add email here to make it mandatory on registration.
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        # The fields shown on the form
        fields = ("username", "email")