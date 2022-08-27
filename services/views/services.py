from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from services.models import Service
from services.serializers import ServiceSerializer, ServiceResponseSerializer
from garage.permissions import DeleteOnlyByAdmin


@extend_schema_view(
    list=extend_schema(
        description='List all services types.'
    ),
    create=extend_schema(
        description='Create a new service type.'
    ),
    retrieve=extend_schema(
        description='Get a service type by id'
    ),
    update=extend_schema(
        description='Update a service type by id.'
    ),
    partial_update=extend_schema(
        description='Partial update a service type by id.'
    ),
    destroy=extend_schema(
        description='Delete a service type by id.\
            \n\n__To use this endpoint, you must be an admin user.__'
    ),
)
@extend_schema_view(
    list=extend_schema(
        responses=ServiceResponseSerializer()
    ),
    retrieve=extend_schema(
        responses=ServiceResponseSerializer()
    ),
)
@extend_schema(tags=['Services'])
class ServicesView(ModelViewSet):
    """
    ViewSet for Service model.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [
        IsAuthenticated,
        DeleteOnlyByAdmin
    ]

    def get_queryset(self):
        queryset = Service.objects.all()\
            .select_related(
                'vehicle',
                'vehicle__client',
                'vehicle__type',
                'vehicle__brand'
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ServiceResponseSerializer
        return self.serializer_class
