from django.db import models

# STEP 4: Define a Simple Book Model
class Book(models.Model):
    """
    A simple model representing a book with a title and an author.
    """
    # Define the fields for the Book model
    title = models.CharField(max_length=250, help_text="Title of the book")
    author = models.CharField(max_length=250, help_text="Author of the book")
    
    def __str__(self):
        # A human-readable representation of the object
        return self.title