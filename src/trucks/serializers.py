from rest_framework import serializers
from .models import Truck, TruckPayment
from orders.serializers import ProductSerializer
from orders.models import Product, Status

from orders.models import PaymentStatus

from orders.serializers import PaymentStatusSerializer


class TruckCreateSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(
        default=0.0, write_only=True
    )

    class Meta:
        model = Truck
        fields = (
            'id', 'full_name',
            'volume', 'payment_amount',
            'created_at', 'payment_status',
            'amount'
        )

    def create(self, validated_data):
        amount = validated_data.pop('amount', 0)
        if amount >= validated_data.get("payment_amount", None):
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="paid",
                defaults={'name': 'Оплачено'}
            )
            instance = Truck.objects.create(
                **validated_data,
                payment_status=payment_status
            )
            TruckPayment.objects.create(
                truck=instance,
                amount=amount,
            )

        elif amount != validated_data.get("payment_amount", None) and amount != 0:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="partially",
                defaults={'name': 'Частично'}
            )
            instance = Truck.objects.create(
                **validated_data,
                payment_status=payment_status
            )
            TruckPayment.objects.create(
                instance=instance,
                amount=amount,
            )
        else:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="not_paid",
                defaults={'name': 'Не оплачено'}
            )
            instance = Truck.objects.create(
                **validated_data,
                payment_status=payment_status
            )
        status, _ = Status.objects.get_or_create(slug="onTheWay", defaults={'name': "В Пути"})
        products = Product.objects.filter(status__slug="loading")
        for product in products:
            product.truck = instance
            product.status = status
            product.save()
        return instance


class TruckPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckPayment
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    payment_status = PaymentStatusSerializer(many=False)
    truck_payments = TruckPaymentSerializer(many=True)

    class Meta:
        model = Truck
        fields = (
            'id', 'full_name',
            'volume', 'products',
            'count_of_products',
            'created_at', 'truck_payments',
            'payment_status',
        )
