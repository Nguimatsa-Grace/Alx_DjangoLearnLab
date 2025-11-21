from django.db import models

# Task 3: Define the Custom Model Manager
class BookManager(models.Manager):
    """
    Custom manager for the Book model.
    """
    def get_dune_books(self):
        """Returns books where the title is exactly 'Dune'."""
        # Use self.filter() to return a QuerySet from the manager
        return self.filter(title='Dune')

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
    # Attach the custom manager to the model, replacing the default Manager
    objects = BookManager()

    def __str__(self):
        return self.title