from rest_framework.pagination import PageNumberPagination
from .settings import REST_FRAMEWORK


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page
    page_size_query_description = f"Number of results to return per page.\
        Default: {REST_FRAMEWORK['PAGE_SIZE']}"

    # def get_paginated_response_schema(self, schema):
    #     response_schema = super(CustomPagination, self).get_paginated_response_schema(schema)
    #     response_schema['properties']['extra'] = {
    #         'type': 'object',
    #         'nullable': True,
    #     }
    #     return response_schema
