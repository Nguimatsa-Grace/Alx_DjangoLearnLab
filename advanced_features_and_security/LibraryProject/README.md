# LibraryProject - Custom Permissions and User Groups

This project implements advanced features focusing on custom permission management and group-based access control using the Django authorization system.

## Key Features Implemented:

### 1. Custom Permissions
Two custom permissions, `can_create` and `can_delete`, have been defined on the **Book** model in `bookshelf/models.py`.

### 2. User Groups
Three primary user groups were created in the Django Admin and assigned distinct permission levels:
* **Admins**: (Superusers) Have unrestricted access.
* **Editors**: Granted **Add**, **Change**, and **Delete** permissions for all relevant models.
* **Viewers**: Granted only the **View** permission for all relevant models.

### 3. Permission Enforcement
The custom permissions are enforced in the `bookshelf/views.py` file using the `@permission_required` decorator on the `create_book` and `delete_book` views, ensuring access control is managed by the group assignments.