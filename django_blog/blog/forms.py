from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects.
    """
    class Meta:
        model = Post
        # We only let users edit title and content; author is set automatically.
        fields = ['title', 'content'] 

class CommentForm(forms.ModelForm):
    """
    A form for creating and updating Comment objects. 
    It only exposes the 'content' field to the user.
    """
    class Meta:
        model = Comment
        fields = ['content']
        # Customize the widget for better presentation
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }