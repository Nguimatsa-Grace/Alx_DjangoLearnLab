# bookshelf/models.py

from django.db import models
from django.conf import settings
# NOTE: We removed the temporary CustomUser, CustomUserManager, AbstractUser, and BaseUserManager imports.

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    
    # Correctly referencing the real custom user model
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 🚨 Task 1 Permissions Definition
    class Meta:
        permissions = [
            ("can_view", "Can view book details"),
            ("can_create", "Can create new books"),
            ("can_edit", "Can edit existing books"),
            ("can_delete", "Can delete books"),
        ]

    def __str__(self):
        return self.title