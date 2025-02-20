from rest_framework.permissions import BasePermission

# Permissions class for handling booking creation, updates, and deletions
class IsAdminOrAuthenticatedCreateUpdateDelete(BasePermission):
    """
    Admins can access everything. Authenticated users can only create, update, delete, and view their own data.
    Unauthenticated users cannot access anything.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.user.is_authenticated and request.method in ["GET", "POST", "PATCH", "DELETE"]

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user

# Permissions class for handling admin and staff access to booking data
class IsAdminOrStaff(BasePermission):
    """
    Admin can edit or delete, staff can only view, others can't access.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return request.user.is_authenticated and request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')
        if request.method in ['PUT', 'DELETE']:
            return request.user.is_authenticated and request.user.role == 'admin'
        return False
