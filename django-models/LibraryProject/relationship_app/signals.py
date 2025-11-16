# relationship_app/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

# Signal receiver function
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # If a new user is created, create a UserProfile
        UserProfile.objects.create(user=instance)
    # If the user is updated, save the profile (optional, but good practice)
    instance.userprofile.save()