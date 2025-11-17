from django.db import models
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

# --- Role Choices for UserProfile ---
ROLE_CHOICES = [
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
    
    def __str__(self): 
        return self.title

    # --- NEW: Custom Permissions (Task 4) ---
    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can edit existing book entries"),
            ("can_delete_book", "Can delete book entries"),
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

# --- NEW: UserProfile for Role-Based Access Control (Task 3) ---

class UserProfile(models.Model):
    # This correctly points to the CustomUser defined in settings.py
    # This fixes the E301 error by using settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    # Role field with predefined choices, defaults to 'Member'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        # We access the email field, which is the USERNAME_FIELD in the custom model
        return f"{self.user.email}'s Profile ({self.role})"