from django.db import models
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

# --- Role Choices for UserProfile ---
ROLE_CHOICES = [
    ('Admin', _('Admin')),  # Added Admin role for Task 3
    ('Librarian', _('Librarian')),
    ('Member', _('Member')),
    ('Guest', _('Guest')),
]

# --- Existing Models ---

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self): 
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default=2000) # Added default year for compatibility
    
    def __str__(self): 
        return self.title

    # --- UPDATED: Custom Permissions (Task 1) ---
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

# --- UserProfile for Role-Based Access Control (Task 3) ---

class UserProfile(models.Model):
    # This correctly points to the CustomUser defined in settings.py
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    # Role field with predefined choices, defaults to 'Member'
    # Ensure 'Admin' is present for Task 3
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        # We access the email field, which is the USERNAME_FIELD in the custom model
        return f"{self.user.username}'s Profile ({self.role})"