from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from services.models import Type
from services.serializers import VehicleTypeSerializer
from garage.permissions import DeleteOnlyByAdmin
from garage.filters import OrderingFilterBackend, SearchFilterBackend


@extend_schema_view(
    list=extend_schema(
        description='List all vehicle types.'
    ),
    create=extend_schema(
        description='Create a new vehicle type.'
    ),
    retrieve=extend_schema(
        description='Get a vehicle type by id'
    ),
    update=extend_schema(
        description='Update a vehicle type by id.'
    ),
    partial_update=extend_schema(
        description='Partial update a vehicle type by id.'
    ),
    destroy=extend_schema(
        description='Delete a vehicle type by id.\
            \n\n__To use this endpoint, you must be an admin user.__'
    ),
)
@extend_schema(tags=['Types'])
class VehicleTypesView(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [
        IsAuthenticated,
        DeleteOnlyByAdmin
    ]
    filter_backends = [
        SearchFilterBackend,
        OrderingFilterBackend
    ]
    search_fields = [
        'name'
    ]
    ordering_fields = [
        'id',
        'name'
    ]
