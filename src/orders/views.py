from rest_framework import generics, viewsets, filters, permissions
from .models import Product, ProductType, Status
from .serializers import (
    StatusSerializer, ProductTypeSerializer,
    ProductSerializer, ProductCreateSerializer
)
from accounts.pagination import CustomPageNumberPagination
from .filters import ProductFilter
from django_filters import rest_framework as dj_filters


class StatusListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = Product.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (dj_filters.DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = ProductFilter
    search_fields = ('receiver_full_name',)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        else:
            return ProductCreateSerializer
