from django.db import models
from datetime import date


class Type(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    date = models.DateField(default=date.today)
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE,
        related_name="expenses"
    )
    comment = models.TextField(blank=True, null=True)
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount)
