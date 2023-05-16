from django.db import models


class Truck(models.Model):
    full_name = models.CharField(max_length=255)
    volume = models.FloatField(default=0.0)
    payment_amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def count_of_products(self):
        return self.products.count()
