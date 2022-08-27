from rest_framework.filters import SearchFilter, OrderingFilter


class SearchFilterBackend(SearchFilter):
    """Custom filter that add search description to the schema"""
    def get_schema_operation_parameters(self, view):
        self.search_description = f'Search in {", ".join(getattr(view, "search_fields", None))}'
        return super().get_schema_operation_parameters(view)


class OrderingFilterBackend(OrderingFilter):
    """Custom filter that add ordering description to the schema"""
    def get_schema_operation_parameters(self, view):
        self.ordering_description = f'Order by {", ".join(getattr(view, "ordering_fields", None))}'
        return super().get_schema_operation_parameters(view)
