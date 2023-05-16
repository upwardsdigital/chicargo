from rest_framework import pagination, response
from .models import Product


class OrderPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return response.Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'loading_orders_count': Product.objects.filter(status__slug="loading").count(),
            'results': data
        })
