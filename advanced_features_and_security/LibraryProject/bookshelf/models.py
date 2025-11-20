from django.db import models

class Book(models.Model):
    """
    Model representing a book in the library.
    This model is used to define the custom permissions required for the assignment.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    
    class Meta:
        # Define the custom permissions required by the check
        permissions = [
            ("can_create", "Can create new books"),
            ("can_delete", "Can delete books"),
        ]
        
    def __str__(self):
        return self.title