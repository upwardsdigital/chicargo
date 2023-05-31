from rest_framework import generics, viewsets, filters, permissions
from .models import Product, ProductType, Status, PackageType
from .serializers import (
    StatusSerializer, ProductTypeSerializer,
    ProductSerializer, ProductCreateSerializer,
    PackageTypeSerializer
)
from accounts.pagination import CustomPageNumberPagination
from .filters import ProductFilter
from django_filters import rest_framework as dj_filters
from .pagination import OrderPageNumberPagination


class StatusListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class PackageTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PackageTypeSerializer
    queryset = PackageType.objects.all()


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = Product.objects.all().order_by('-id')
    pagination_class = OrderPageNumberPagination
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


class ProductHistoryListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = Product.objects.filter(status__slug="issued").order_by('-id')
    pagination_class = OrderPageNumberPagination
    filter_backends = (dj_filters.DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = ProductFilter
    serializer_class = ProductSerializer
    search_fields = ('receiver_full_name',)
