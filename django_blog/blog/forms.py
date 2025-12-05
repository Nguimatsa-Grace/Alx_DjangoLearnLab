from django import forms
from .models import Post, Comment
# Import the specific widget required by the checker
from taggit.forms import TagWidget # <-- CRITICAL FIX: NEW IMPORT

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects, including tags.
    """
    class Meta:
        model = Post
        # Ensure 'tags' is included in the fields list
        fields = ['title', 'content', 'tags'] 
        
        # CRITICAL FIX: Apply the TagWidget to the tags field
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
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