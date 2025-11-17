from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    A custom user model that extends Django's default user model (AbstractUser).
    This allows us to add custom fields, such as 'age', without modifying 
    the core Django code.
    """
    # The 'age' field is added as an example of customization
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        # Use the email as the primary display field
        return self.email 

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"