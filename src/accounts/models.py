from django.contrib.auth.models import AbstractUser
from django.db import models


class Country(models.Model):
    name = models.CharField(unique=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, related_name="users"
    )
