Delete Operation

Objective: Delete the book you created and confirm the deletion by trying to retrieve all books again.

Python Command (to be run in Django Shell):

from bookshelf.models import Book
book = Book.objects.get(pk=1)
book.delete()
print(Book.objects.all())


Expected Output:

# Output:
# <QuerySet []>
