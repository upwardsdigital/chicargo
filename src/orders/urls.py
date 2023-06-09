from django.urls import path, include
from rest_framework import routers

from .views import (
    StatusListCreateAPIView, ProductTypeListCreateAPIView,
    ProductModelViewSet, ProductHistoryListAPIView,
    PackageTypeListCreateAPIView, CalculateDebtAmountAPIView,
    PaymentStatusListCreateAPIView,
    PaymentRetrieveDestroyAPIView, PaymentRetrieveDestroyAPIView
)

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")

urlpatterns = [
    path('statuses/', StatusListCreateAPIView.as_view(), name="statuses"),
    path('payment/statuses/', PaymentStatusListCreateAPIView.as_view(), name="payment_statuses"),
    path('products/types/', ProductTypeListCreateAPIView.as_view(), name="products_types"),
    path('products/history/', ProductHistoryListAPIView.as_view(), name="products_history"),
    path('products/package/types/', PackageTypeListCreateAPIView.as_view(), name="package_types"),
    path('', include(router.urls)),
    path(
        'products/calculate/payment/amount/',
        CalculateDebtAmountAPIView.as_view(),
        name="product_payment_amount_calculate"
    ),
    path(
        'transaction/<int:pk>/',
        PaymentRetrieveDestroyAPIView.as_view(),
        name="transaction"
    )
]
