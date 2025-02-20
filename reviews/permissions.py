from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allow read-only access for everyone.
    Only the review's owner can edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # Allow GET requests for all
            return True
        return obj.user == request.user  # Only owner can edit/delete
