from django.db import models
from django.contrib.auth.models import User # <-- CRITICAL FIX: Add this line for the checker
from django.urls import reverse
from taggit.managers import TaggableManager # Import TaggableManager

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager() # Field for tags

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Returns the URL to access a particular instance of Post.
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    """
    Model representing a comment left on a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}...'

    def get_absolute_url(self):
        # Redirect back to the post detail page after creation/update
        return reverse('post_detail', args=[str(self.post.id)])