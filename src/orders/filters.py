from django_filters import rest_framework as dj_filters
from .models import Product


class ProductFilter(dj_filters.FilterSet):
    start_created_at = dj_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    end_created_at = dj_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Product
        fields = (
            "status",
            "start_created_at",
            "end_created_at"
        )
