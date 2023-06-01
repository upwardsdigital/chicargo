from django.db import models

from orders.models import PaymentStatus


class Truck(models.Model):
    full_name = models.CharField(max_length=255)
    volume = models.FloatField(default=0.0)
    payment_amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,
        related_name="trucks",
        blank=True, null=True
    )

    def __str__(self):
        return self.full_name

    def count_of_products(self):
        return self.products.count()

    def total_paid_amount(self):
        return sum(
            [payment.amount for payment in self.truck_payments.all()]
        )


class TruckPayment(models.Model):
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        related_name="truck_payments"
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.date)
