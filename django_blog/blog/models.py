# File: myblog/models.py

from django.db import models
from django.contrib.auth.models import User # Required for the author field

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    # The Foreign Key links a post to a User
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title