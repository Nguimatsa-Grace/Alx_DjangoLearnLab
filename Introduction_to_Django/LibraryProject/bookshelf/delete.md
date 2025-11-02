### Delete Operation

**Objective:** Delete the book you created and confirm the deletion by trying to retrieve all books again.

**Python Command (to be run in Django Shell):**
```python
from bookshelf.models import Book
book_to_delete = Book.objects.get(pk=1)
book_to_delete.delete()
print(Book.objects.all())
Expected Output:

# Output:
# <QuerySet []>

