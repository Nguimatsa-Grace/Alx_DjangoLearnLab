# File: blog/forms.py (Updated with PostForm)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post # Import the Post model

# --- Q1: Custom User Creation Form ---
class CustomUserCreationForm(UserCreationForm):
    # ... (Q1 code remains here) ...
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ("username", "email") 


# --- Q2: Post Management Form ---
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # We only need title and content fields for the form. 
        # The author field will be set automatically in the view.
        fields = ['title', 'content']