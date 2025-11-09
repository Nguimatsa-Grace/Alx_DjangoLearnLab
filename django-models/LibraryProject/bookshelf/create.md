Create Operation

Objective: Create a Book instance with the title “1984”, author “George Orwell”, and publication year 1949.

Python Command (to be run in Django Shell):

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)


Expected Output:

# Output:
# 1984 by George Orwell (1949)
