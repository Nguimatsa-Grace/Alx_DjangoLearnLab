# relationship_app/models.py (Replace the entire file content with this)

from django.db import models
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    # ForeignKey: One Author to Many Books
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self): return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    # ManyToManyField: Many Libraries to Many Books
    books = models.ManyToManyField(Book)
    def __str__(self): return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    # OneToOneField: One Library to One Librarian
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    def __str__(self): return self.name