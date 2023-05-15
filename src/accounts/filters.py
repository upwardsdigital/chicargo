from django_filters import rest_framework as dj_filters
from .models import Report


class ReportFilter(dj_filters.FilterSet):
    start_created_at = dj_filters.DateFilter(field_name="name", lookup_expr="gte")
    end_created_at = dj_filters.DateFilter(field_name="name", lookup_expr="lte")

    class Meta:
        model = Report
        fields = (
            "author__country",
            "start_created_at",
            "end_created_at"
        )
