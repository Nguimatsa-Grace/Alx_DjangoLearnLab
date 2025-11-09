Retrieve Operation

Objective: Retrieve and display all attributes of the book you just created.

Python Command (to be run in Django Shell):

from bookshelf.models import Book
# Assuming the book created above has a primary key (id) of 1
retrieved_book = Book.objects.get(pk=1)
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Year: {retrieved_book.publication_year}")


Expected Output:

# Output:
# Title: 1984
# Author: George Orwell
# Year: 1949
