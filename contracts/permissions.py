
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthenticatedCreateUpdateDelete(BasePermission):
    """
    Custom permission to allow anyone to read,
    but only admin or authenticated users to create/update/delete.
    """

    def has_permission(self, request, view):
 
        return request.user.is_staff or getattr(request.user, "role", None) == "admin"
