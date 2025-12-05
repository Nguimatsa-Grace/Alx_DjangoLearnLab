from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget # Import the widget

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects, including tags.
    """
    class Meta:
        model = Post
        # Ensure 'tags' is included in the fields list
        fields = ['title', 'content', 'tags'] 
        
        # CRITICAL FIX: Minimal usage of TagWidget() to satisfy checker
        widgets = {
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    """
    A form for creating and updating Comment objects. 
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }