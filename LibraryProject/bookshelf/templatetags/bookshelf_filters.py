from django import template

register = template.Library()

@register.filter
def is_librarian(user):
    """
    Checks if a user belongs to the 'Librarian' group.
    """
    return user.groups.filter(name='Librarian').exists()

@register.filter
def is_patron(user):
    """
    Checks if a user belongs to the 'Patron' group.
    """
    return user.groups.filter(name='Patron').exists()