from rest_framework.permissions import BasePermission, SAFE_METHODS


class ManageOnlyByCurrentUser(BasePermission):
    """Check if request user try to retrieve or update their own user."""
    message = 'You haven\'t permission to manage this object.'

    def has_permission(self, request, view):
        user_id = view.kwargs.get('pk')
        if not user_id or request.method in SAFE_METHODS:
            return True

        return int(user_id) == request.user.id
