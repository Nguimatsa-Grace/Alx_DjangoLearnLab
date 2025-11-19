# relationship_app/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Task 0 Models (Relationships) ---

class Author(models.Model):
    name = models.CharField(max_length=100)
    # ... (other code for Author)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default=2000)
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book entry"),
            ("can_change_book", "Can change book entry"),
            ("can_delete_book", "Can delete book entry"),
        ]
    # ... (other code for Book)

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    # ... (other code for Library)

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    # ... (other code for Librarian)

# --- Task 3 Model (Role-Based Access Control) ---

ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    # ... (other code for UserProfile)

# Task 3: Automatic Creation using Signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()