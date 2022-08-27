from rest_framework.permissions import BasePermission


class DeleteOnlyByAdmin(BasePermission):
    message = 'You haven\'t permission to delete this object.'

    def has_permission(self, request, view):
        if view.action == 'destroy':
            return request.user.is_staff

        return True
