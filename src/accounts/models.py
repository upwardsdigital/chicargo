from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class Country(models.Model):
    name = models.CharField(unique=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING,
        related_name="users",
        blank=True, null=True
    )


class Report(models.Model):
    name = models.DateField(default=date.today)
    users = models.ManyToManyField(
        User, related_name="reports"
    )
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        blank=True, null=True
    )

    def __str__(self):
        return str(self.name)
