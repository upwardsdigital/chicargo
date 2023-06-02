from django.urls import path
from .views import (
    TruckListCreateAPIView, TruckPaymentRetrieveDestroyAPIView, CalculateTruckDebtAmountAPIView,
    TruckRetrieveUpdateAPIView, TruckProductListAPIView
)


urlpatterns = [
    path('trucks/', TruckListCreateAPIView.as_view(), name="trucks"),
    path('trucks/<int:pk>/', TruckRetrieveUpdateAPIView.as_view(), name="truck"),
    path('trucks/<int:pk>/products/', TruckProductListAPIView.as_view(), name="truck_products"),
    path('trucks/transaction/<int:pk>/', TruckPaymentRetrieveDestroyAPIView.as_view()),
    path('trucks/payment/calculate/', CalculateTruckDebtAmountAPIView.as_view()),
]
