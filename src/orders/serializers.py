from rest_framework import serializers
from .models import Product, ProductType, Status, PackageType, Payment, PaymentStatus
from accounts.serializers import StaffUserSerializer


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class PaymentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentStatus
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
    amount = serializers.FloatField(
        default=0.0, write_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id", "author", "truck",
            "sender_full_name", "sender_phone",
            "receiver_full_name", "receiver_phone",
            "city", "type", "package_type", "address",
            "price", "status", "payment_status", "quantity", "created_at",
            "amount"
        )

    def create(self, validated_data):
        amount = validated_data.pop("amount", 0)
        status, _ = Status.objects.get_or_create(
            slug="loading",
            defaults={'name': 'Погрузка'}
        )
        if amount >= validated_data.get("price", None):
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="paid",
                defaults={'name': 'Оплачено'}
            )
            product = Product.objects.create(
                **validated_data,
                status=status,
                payment_status=payment_status
            )
            Payment.objects.create(
                product=product,
                amount=amount
            )

        elif amount != validated_data.get("price", None) and amount != 0:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="partially",
                defaults={'name': 'Частично'}
            )
            product = Product.objects.create(
                **validated_data,
                status=status,
                payment_status=payment_status
            )
            Payment.objects.create(
                product=product,
                amount=amount
            )
        else:
            payment_status, _ = PaymentStatus.objects.get_or_create(
                slug="not_paid",
                defaults={'name': 'Не оплачено'}
            )
            product = Product.objects.create(
                **validated_data,
                status=status,
                payment_status=payment_status
            )
        return product

    def update(self, instance, validated_data):
        amount = validated_data.pop("amount", 0)
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = serializers.model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        if amount != 0:
            Payment.objects.create(
                product=instance,
                amount=amount
            )

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


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
    payment_status = PaymentStatusSerializer(many=False)

    class Meta:
        model = Product
        fields = (
            'id', 'author',
            'truck', 'sender_full_name',
            'sender_phone', 'receiver_full_name',
            'receiver_phone', 'city',
            'type', 'package_type',
            'address', 'price', 'status',
            'payments', 'payment_status',
            'quantity', 'created_at',
            'total_paid_amount'
        )

