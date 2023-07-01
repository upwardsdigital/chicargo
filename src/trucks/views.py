from rest_framework import generics, permissions, views, response, status
from django.shortcuts import get_object_or_404
from .serializers import (
    TruckSerializer, TruckCreateSerializer,
    TruckPaymentSerializer, TruckStatusSerializer
)
from orders.serializers import ProductSerializer
from .models import Truck, TruckPayment, TruckStatus
from .filters import TruckFilter
from accounts.pagination import CustomPageNumberPagination

from orders.models import Product


class TruckListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    queryset = Truck.objects.all().order_by('-id')
    filterset_class = TruckFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TruckCreateSerializer
        else:
            return TruckSerializer


class TruckRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Truck.objects.all().order_by('-id')
    # permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TruckSerializer
        else:
            return TruckCreateSerializer


class TruckPaymentRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = TruckPaymentSerializer
    queryset = TruckPayment.objects.all()


class TruckProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        truck_id = self.kwargs['pk']
        queryset = Product.objects.filter(truck_id=truck_id)
        return queryset


class CalculateTruckDebtAmountAPIView(views.APIView):

    def post(self, request):
        truck_id = request.data.get("truck_id", None)
        if truck_id is not None:
            truck = get_object_or_404(Truck, pk=truck_id)
            debt_amount = truck.payment_amount - sum(
                [truck_payment.amount for truck_payment in truck.truck_payments.all()]
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
                    "message": "truck_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TruckStatusListAPIView(generics.ListAPIView):
    serializer_class = TruckStatusSerializer
    queryset = TruckStatus.objects.all()
