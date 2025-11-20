from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

# The newly added view required by the check
def book_list(request):
    """
    Placeholder view for listing books, usually accessible by all users.
    """
    return HttpResponse("This is the book list page.")


# The custom permission views defined earlier
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    View that requires the custom 'can_create' permission.
    Admins and Editors should have access.
    """
    return HttpResponse("You have permission to create books.")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    """
    View that requires the custom 'can_delete' permission.
    Admins and Editors should have access.
    """
    return HttpResponse("You have permission to delete books.")