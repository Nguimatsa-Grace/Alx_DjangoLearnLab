from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

# --- Custom User Manager (Step 3) ---
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier 
    and handles custom field requirements.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email, date_of_birth, and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not extra_fields.get('date_of_birth'):
            raise ValueError(_('The Date of Birth must be set'))
            
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # Superuser creation requires all fields in REQUIRED_FIELDS.
        # Ensure a default date_of_birth if one isn't provided (for consistency)
        if 'date_of_birth' not in extra_fields:
             # Use a placeholder date for administrative users if not provided
            extra_fields['date_of_birth'] = datetime.date(1900, 1, 1)

        return self.create_user(email, password, **extra_fields)


# --- Custom User Model (Step 1) ---
class CustomUser(AbstractUser):
    """
    A custom User model based on AbstractUser, using email for login
    and adding custom fields: date_of_birth and profile_photo.
    """
    # Overriding standard fields for custom use
    username = None # Remove the default username field
    email = models.EmailField(_('email address'), unique=True)
    
    # Custom Fields to Add:
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True, 
        blank=True
    )
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/', 
        null=True, 
        blank=True
    )

    # Configuration settings for authentication
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    # These fields will be asked when running `createsuperuser`
    REQUIRED_FIELDS = ['date_of_birth'] 

    def __str__(self):
        return self.email