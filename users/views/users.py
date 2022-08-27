from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.serializers import UsersSerializer
from garage.permissions import DeleteOnlyByAdmin
from users.permissions import ManageOnlyByCurrentUser


permission_admin_text = '\n\n__To use this endpoint, you must be an admin user.__'
permission_user_text = '\n\n__To use this endpoint, you must be admin or the current user.__'


@extend_schema_view(
    list=extend_schema(
        description=f'List all users. {permission_admin_text}'
    ),
    create=extend_schema(
        description=f'Create a new user. {permission_admin_text}'
    ),
    retrieve=extend_schema(
        description=f'Get a user by id. {permission_user_text}'
    ),
    update=extend_schema(
        description=f'Update a user by id. {permission_user_text}'
    ),
    partial_update=extend_schema(
        description=f'Partial update a user by id. {permission_user_text}'
    ),
    destroy=extend_schema(
        description=f'Delete a user by id. {permission_admin_text}'
    ),
)
@extend_schema(tags=['Users'])
class UsersView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser | ManageOnlyByCurrentUser,
        DeleteOnlyByAdmin
    ]
