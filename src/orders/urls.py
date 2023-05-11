from django.urls import path, include
from rest_framework import routers

from .views import (
    StatusListCreateAPIView, ProductTypeListCreateAPIView,
    ProductModelViewSet
)

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet, basename="products")

urlpatterns = [
    path('statuses/', StatusListCreateAPIView.as_view(), name="statuses"),
    path('products/types/', ProductTypeListCreateAPIView.as_view(), name="product_types"),
    path('', include(router.urls))
]
