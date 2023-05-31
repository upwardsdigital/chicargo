from rest_framework import serializers
from .models import Product, ProductType, Status, PackageType, Payment
from accounts.serializers import StaffUserSerializer


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class PackageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageType
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(default=0.0, write_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "author", "truck",
            "sender_full_name", "sender_phone",
            "receiver_full_name", "receiver_phone",
            "city", "type", "package_type", "address",
            "price", "status", "quantity", "created_at",
            "amount"
        )

    def create(self, validated_data):
        amount = validated_data.pop("amount", 0)
        if amount != 0:
            status, _ = Status.objects.get_or_create(
                slug="partially",
                defaults={'name': 'Оплачен частично'}
            )
            product = Product.objects.create(
                **validated_data,
                status=status
            )
            Payment.objects.create(
                product=product,
                amount=amount
            )
        else:
            status, _ = Status.objects.get_or_create(
                slug="loading",
                defaults={'name': 'Погрузка'}
            )
            product = Product.objects.create(
                **validated_data,
                status=status
            )
        return product


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    author = StaffUserSerializer(many=False)
    status = StatusSerializer(many=False)
    type = ProductTypeSerializer(many=False)
    package_type = PackageTypeSerializer(many=False)
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

