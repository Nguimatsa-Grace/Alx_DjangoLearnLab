from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """
    Model used to demonstrate custom permissions and group-based access control.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        # Define the custom permissions here
        permissions = [
            ("can_view", "Can view project details"),
            ("can_create", "Can create new projects"),
            ("can_edit", "Can edit existing projects"),
            ("can_delete", "Can delete projects"),
        ]

    def __str__(self):
        return self.title