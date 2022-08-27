from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from services.serializers import ClientsSerializer
from services.models import Client
from garage.permissions import DeleteOnlyByAdmin
from garage.filters import OrderingFilterBackend, SearchFilterBackend


@extend_schema_view(
    list=extend_schema(
        description='List all clients.'
    ),
    create=extend_schema(
        description='Create a new client.'
    ),
    retrieve=extend_schema(
        description='Get a client by id'
    ),
    update=extend_schema(
        description='Update a client by id.'
    ),
    partial_update=extend_schema(
        description='Partial update a client by id.'
    ),
    destroy=extend_schema(
        description='Delete a client by id.\
            \n\n__To use this endpoint, you must be an admin user.__'
    ),
)
@extend_schema(tags=['Clients'])
class ClientsView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientsSerializer
    permission_classes = [
        IsAuthenticated,
        DeleteOnlyByAdmin
    ]
    filter_backends = [
        SearchFilterBackend,
        OrderingFilterBackend
    ]
    search_fields = [
        'last_name',
        'first_name',
        'email'
    ]
    ordering_fields = [
        'id',
        'last_name',
        'is_active'
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
