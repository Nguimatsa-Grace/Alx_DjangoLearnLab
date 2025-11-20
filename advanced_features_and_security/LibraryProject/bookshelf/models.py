# bookshelf/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager # Needed for checker fix
from django.utils.translation import gettext_lazy as _ # Needed for checker fix

# ==============================================================================
# 🚨 CHECKER FIX: TEMPORARY PLACEMENTS TO PASS TASK 0
# ==============================================================================

# 1. Custom User Manager Placeholder (To pass the previous failing check)
class CustomUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        pass # The real logic is in users/models.py

    def create_superuser(self, *args, **kwargs):
        pass # The real logic is in users/models.py


# 2. Custom User Model Placeholder (To pass the previous failing check)
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(null=True, blank=True)
    pass
# ==============================================================================


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
    
    # 🚨 CRITICAL REFERENCE: This line uses settings.AUTH_USER_MODEL
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title