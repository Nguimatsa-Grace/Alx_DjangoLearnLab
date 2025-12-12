from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Requirement for Task 0: bio must be models.TextField
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Task 0 asks for 'followers', Task 2 asks for 'following'
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_followers')
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_following')

    def __str__(self):
        return self.username