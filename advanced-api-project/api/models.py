from django.db import models

# Create your models here.
# Step 3: Define Data Models

class Author(models.Model):
    """
    Model definition for an Author.
    This model serves as the 'one' side of the one-to-many relationship,
    meaning one Author can be associated with multiple Books.
    
    Fields:
    - name: Stores the author’s full name.
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="Author Name",
        help_text="The full name of the author."
    )

    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    class Meta:
        verbose_name_plural = "Authors"

class Book(models.Model):
    """
    Model definition for a Book.
    This model serves as the 'many' side, linking back to the Author.
    
    Fields:
    - title: The title of the book.
    - publication_year: The year the book was published (used later for validation).
    - author: A Foreign Key linking this book to an Author.
    
    The 'related_name="books"' argument is crucial, as it allows us to easily 
    access all books of an author (e.g., author_instance.books.all()) in our serializers, 
    which is essential for the nested serializer in Step 4.
    """
    title = models.CharField(
        max_length=255, 
        verbose_name="Book Title",
        help_text="The official title of the book."
    )
    
    publication_year = models.IntegerField(
        verbose_name="Publication Year",
        help_text="The year the book was published (e.g., 2024)."
    )
    
    # Foreign Key relationship (one-to-many)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books', # Key for nested serialization
        verbose_name="Author"
    )

    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['publication_year', 'title']