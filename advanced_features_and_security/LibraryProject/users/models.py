from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- Custom User Manager (Handles user creation using email) ---
class CustomUserManager(BaseUserManager):
    """
    Custom manager to use email as the unique identifier for authentication.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a Superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# --- Custom User Model (Extends default user) ---
class CustomUser(AbstractUser):
    # Overriding the default email field to make it unique and mandatory
    email = models.EmailField(_('email address'), unique=True)
    
    # Custom fields: date_of_birth and profile_photo
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
        help_text="User's profile image (Requires Pillow library)."
    )

    # Telling Django to use the 'email' field for login/authentication
    USERNAME_FIELD = 'email'
    
    # Fields that will be prompted when creating a user via createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name'] 
    
    # Assign the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email