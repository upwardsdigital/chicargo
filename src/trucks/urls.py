from django.urls import path
from .views import TruckListCreateAPIView, TruckPaymentRetrieveDestroyAPIView, CalculateTruckDebtAmountAPIView


urlpatterns = [
    path('trucks/', TruckListCreateAPIView.as_view(), name="trucks"),
    path('trucks/transaction/<int:pk>/', TruckPaymentRetrieveDestroyAPIView.as_view()),
    path('trucks/payment/calculate/', CalculateTruckDebtAmountAPIView.as_view()),
]
