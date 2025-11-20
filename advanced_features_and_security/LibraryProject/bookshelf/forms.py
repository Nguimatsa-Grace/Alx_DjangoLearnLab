# bookshelf/forms.py
from django import forms
from .models import Book

# This form is required by the check to demonstrate form-based validation/sanitization.
class ExampleForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        # Example of built-in validation and sanitization
        help_text="Max 100 characters. Input will be sanitized by Django's form processing.",
        required=True
    )
    author_name = forms.CharField(max_length=50)

    # You could also use a ModelForm for better integration:
    # class Meta:
    #     model = Book
    #     fields = ['title', 'author', 'publication_date', 'isbn']