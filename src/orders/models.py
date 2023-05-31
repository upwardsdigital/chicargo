from django.db import models
from django.contrib.auth import get_user_model
from trucks.models import Truck


User = get_user_model()


class Status(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PaymentStatus(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PackageType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="products",
        blank=True, null=True
    )
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE,
        related_name="products",
        blank=True, null=True
    )
    sender_full_name = models.CharField(max_length=255)
    sender_phone = models.CharField(max_length=255)
    receiver_full_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="products"
    )
    package_type = models.ForeignKey(
        PackageType, on_delete=models.CASCADE,
        related_name="products",
        blank=True, null=True
    )
    address = models.CharField(max_length=255)
    price = models.FloatField()
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True, null=True
    )
    payment_status = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True, null=True
    )
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender_full_name

    def total_paid_amount(self):
        return sum(
            [payment.amount for payment in self.payments.all()]
        )


class Payment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    staff = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.date)
