from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.serializers import UsersSerializer
from garage.permissions import DeleteOnlyByAdmin
from users.permissions import ManageOnlyByCurrentUser

class UsersView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser | ManageOnlyByCurrentUser,
        DeleteOnlyByAdmin
    ]
