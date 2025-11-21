from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=200, help_text="Title of the book.")
    author = models.CharField(max_length=100, help_text="Name of the author.")
    isbn = models.CharField(max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # Optional link to a cover image (URL field)
    cover_url = models.URLField(max_length=200, blank=True, null=True, help_text="Optional link to the book cover image.")
    
    # Status fields for checkout
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title', 'author']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        """
        Returns a string representation of the model (Title by Author).
        """
        return f'{self.title} by {self.author}'