# relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User 

# --- Existing Models ---

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): 
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default=2000) # Added default year for consistency
    
    def __str__(self): 
        return self.title

    # --- TASK 1: Custom Permissions (Mandatory) ---
    # These must match the exact names: can_view, can_create, can_edit, can_delete
    class Meta:
        permissions = [
            ("can_view", "Can view book entries"),
            ("can_create", "Can create a new book entry"),
            ("can_edit", "Can edit existing book entries"),
            ("can_delete", "Can delete book entries"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    def __str__(self): 
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    def __str__(self): 
        return self.name

# --- UserProfile (For future role-based tasks) ---

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"