from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Status(models.Model):
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
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender_full_name
