from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

# The custom permissions we defined in models.py are used here
# to restrict access to these functions.

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