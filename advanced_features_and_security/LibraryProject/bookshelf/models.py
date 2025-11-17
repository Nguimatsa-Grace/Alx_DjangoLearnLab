from django.db import models

# --- Author Model ---
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# --- Book Model ---
class Book(models.Model):
    title = models.CharField(max_length=100)
    # The 'author' field links to the Author model
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author.first_name} {self.author.last_name} ({self.publication_year})"