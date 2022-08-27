from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from services.models import Brand
from services.serializers import BrandSerializer
from garage.permissions import DeleteOnlyByAdmin


@extend_schema_view(
    list=extend_schema(
        description='List all brands.'
    ),
    create=extend_schema(
        description='Create a new brand.'
    ),
    retrieve=extend_schema(
        description='Get a brand by id'
    ),
    update=extend_schema(
        description='Update a brand by id.'
    ),
    partial_update=extend_schema(
        description='Partial update a brand by id.'
    ),
    destroy=extend_schema(
        description='Delete a brand by id.\
            \n\n__To use this endpoint, you must be an admin user.__'
    )
)
@extend_schema(tags=['Brands'])
class BrandsView(ModelViewSet):
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer
    permission_classes = [
        IsAuthenticated,
        DeleteOnlyByAdmin
    ]
