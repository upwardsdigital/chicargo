from django.urls import path, include
from rest_framework import routers

from .views import (
    StatusListCreateAPIView, ProductTypeListCreateAPIView,
    ProductModelViewSet, ProductHistoryListAPIView,
    PackageTypeListCreateAPIView
)

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")

urlpatterns = [
    path('statuses/', StatusListCreateAPIView.as_view(), name="statuses"),
    path('products/types/', ProductTypeListCreateAPIView.as_view(), name="products_types"),
    path('products/history/', ProductHistoryListAPIView.as_view(), name="products_history"),
    path('products/package/types/', PackageTypeListCreateAPIView.as_view(), name="package_types"),
    path('', include(router.urls))
]
