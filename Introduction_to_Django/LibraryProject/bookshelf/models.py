from django.db import models

# --- New Model for Task 3: Author ---
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# --- Updated Book Model with Foreign Key ---
class Book(models.Model):
    title = models.CharField(max_length=100)
    # The 'author' field now links to the Author model (one-to-many relationship)
    # on_delete=models.CASCADE means if an Author is deleted, all their books are deleted too.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author.first_name} {self.author.last_name} ({self.publication_year})"