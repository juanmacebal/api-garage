from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from services.models import Vehicle
from services.serializers import VehiclesSerializer, VehiclesResponseSerializer
from garage.permissions import DeleteOnlyByAdmin
from garage.filters import OrderingFilterBackend, SearchFilterBackend


@extend_schema_view(
    list=extend_schema(
        description='List all vehicles.',
    ),
    create=extend_schema(
        description='Create a new vehicle.'
    ),
    retrieve=extend_schema(
        description='Get a vehicle by id'
    ),
    update=extend_schema(
        description='Update a vehicle by id.'
    ),
    partial_update=extend_schema(
        description='Partial update a vehicle by id.'
    ),
    destroy=extend_schema(
        description='Delete a vehicle by id.\
            \n\n__To use this endpoint, you must be an admin user.__'
    ),
)
@extend_schema_view(
    list=extend_schema(
        responses=VehiclesResponseSerializer()
    ),
    retrieve=extend_schema(
        responses=VehiclesResponseSerializer()
    ),
)
@extend_schema(tags=['Vehicles'])
class VehiclesView(ModelViewSet):
    queryset = Vehicle.objects.all()\
        .select_related(
            'client',
            'type',
            'brand'
        )  # noqa
    serializer_class = VehiclesSerializer
    permission_classes = [IsAuthenticated, DeleteOnlyByAdmin]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilterBackend,
        OrderingFilterBackend
    ]
    filterset_fields = [
        'type',
        'brand',
        'model'
    ]
    search_fields = [
        'type',
        'brand',
        'model',
        'license_plate',
        'year',
        'client__last_name',
        'client__first_name',
    ]
    ordering_fields = [
        'id',
        'type',
        'brand',
        'model',
        'year'
    ]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return VehiclesResponseSerializer
        return self.serializer_class
