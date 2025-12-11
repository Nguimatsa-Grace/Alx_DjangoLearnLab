# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Standard AbstractUser fields (username, email, password, etc.) are included automatically.

    # This field creates the many-to-many relationship for following.
    # 'self' refers to the CustomUser model itself.
    # 'symmetrical=False' means if A follows B, B does not automatically follow A.
    # 'related_name' allows us to find who follows a user (e.g., user.followers.all())
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers', 
        blank=True
    )
    
    # You can add other custom fields here if needed, like 'profile_picture'
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']