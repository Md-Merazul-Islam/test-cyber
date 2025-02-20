
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrAuthenticatedCreateUpdateDelete(BasePermission):
    """
    Custom permission to allow anyone to read,
    but only admin or authenticated users to create/update/delete.
    """
    
    def has_permission(self, request, view):
            if request.method in SAFE_METHODS:
                return True  # Allow read access for everyone
            
            # Ensure user is authenticated before checking attributes
            if not request.user.is_authenticated:
                return False 
            
            # Allow if the user is staff or has role='admin'
            return request.user.is_staff or getattr(request.user, "role", None) == "admin"