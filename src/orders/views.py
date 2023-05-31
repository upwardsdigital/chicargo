from django.shortcuts import get_object_or_404
from django_filters import rest_framework as dj_filters
from rest_framework import (
    generics, viewsets, filters, permissions,
    views, response, status
)

from .filters import ProductFilter
from .models import Product, ProductType, Status, PackageType, PaymentStatus
from .pagination import OrderPageNumberPagination
from .serializers import (
    StatusSerializer, ProductTypeSerializer,
    ProductSerializer, ProductCreateSerializer,
    PackageTypeSerializer, PaymentStatusSerializer
)


class StatusListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class PaymentRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = PaymentStatusSerializer
    queryset = PaymentStatus.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = get_object_or_404(Product, pk=instance.product.pk)
        self.perform_destroy(instance)
        transactions = product.payments.all()
        if transactions.count() == 0:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="not_paid",
                defaults={'name': 'Не оплачено'}
            )
            product.payment_status = payment_status
        elif product.price <= sum([payment.amount for payment in transactions]):
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="paid",
                defaults={'name': 'Оплачено'}
            )
            product.payment_status = payment_status
        else:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="partially",
                defaults={'name': 'Оплачен частично'}
            )
            product.payment_status = payment_status
        return response.Response(status=status.HTTP_204_NO_CONTENT)




class PaymentStatusListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentStatusSerializer
    queryset = PaymentStatus.objects.all()


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


class CalculateDebtAmountAPIView(views.APIView):

    def post(self, request):
        product_id = request.data.get("product_id", None)
        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
            debt_amount = product.price - sum(
                [payment.amount for payment in product.payments.all()]
            )
            return response.Response(
                {
                    "debt_amount": debt_amount
                },
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                {
                    "message": "product_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductHistoryListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = Product.objects.filter(status__slug="issued").order_by('-id')
    pagination_class = OrderPageNumberPagination
    filter_backends = (dj_filters.DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = ProductFilter
    serializer_class = ProductSerializer
    search_fields = ('receiver_full_name',)
