from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects.
    """
    class Meta:
        model = Post
        # Add 'tags' field here for django-taggit to manage tag input <-- UPDATED
        fields = ['title', 'content', 'tags'] 

class CommentForm(forms.ModelForm):
    """
    A form for creating and updating Comment objects. 
    It only exposes the 'content' field to the user.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }