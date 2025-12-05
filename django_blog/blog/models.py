from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager # <-- NEW IMPORT

# Get the custom User model (Auth)
User = get_user_model()

class Post(models.Model):
    """
    Model for a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Tagging Manager (django-taggit handles the M2M relationship) <-- NEW FIELD
    tags = TaggableManager()
    
    # Timestamps
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to access a particular instance of the post.
        """
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Model for comments associated with a Post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:30]}...'

    class Meta:
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"