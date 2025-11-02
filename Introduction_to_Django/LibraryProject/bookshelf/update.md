### Update Operation

**Objective:** Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

**Python Command (to be run in Django Shell):**
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(pk=1)
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(book_to_update.title)
Expected Output:

# Output:
# Nineteen Eighty-Four
