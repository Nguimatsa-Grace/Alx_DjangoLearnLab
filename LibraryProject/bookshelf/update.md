Update Operation

Objective: Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

Python Command (to be run in Django Shell):

from bookshelf.models import Book
book = Book.objects.get(pk=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)


Expected Output:

# Output:
# Nineteen Eighty-Four
