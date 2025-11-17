from django.contrib import admin
from .models import Book, Author # <-- Imported Author here

# Register the Author model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Display the first and last names in the list view
    list_display = ('first_name', 'last_name')
    # Allow searching by name
    search_fields = ('first_name', 'last_name')

# Re-register the Book model (unchanged from Task 2)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Now includes 'author' in the display list
    list_display = ('title', 'author', 'publication_year')
    # Can filter by author and year
    list_filter = ('author', 'publication_year')
    # Can search by title and author's name
    search_fields = ('title', 'author__first_name', 'author__last_name')