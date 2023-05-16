from django_filters import rest_framework as dj_filters
from .models import Truck


class TruckFilter(dj_filters.FilterSet):
    start_created_at = dj_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_created_at = dj_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Truck
        fields = (
            "start_created_at",
            "end_created_at"
        )
