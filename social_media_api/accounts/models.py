from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Field names and types required by Task 0 and Task 2
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # followers for Task 0, following for Task 2
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_followers')
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_following')

    def __str__(self):
        return self.username