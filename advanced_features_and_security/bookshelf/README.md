# Permissions and Groups Setup

This Django project uses custom permissions and groups to control access to the Article model.

## Custom Permissions
- `can_view`: Allows viewing of articles.
- `can_create`: Allows creating new articles.
- `can_edit`: Allows editing existing articles.
- `can_delete`: Allows deleting articles.

## Groups
- **Viewers**: Can view articles.
- **Editors**: Can view, create, and edit articles.
- **Admins**: Full control over articles (view, create, edit, delete).

## Enforcing Permissions
Permissions are enforced in views using the `@permission_required` decorator.

Ensure users are assigned to the correct groups to access specific functionalities within the application.
