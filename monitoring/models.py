import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Marketplace(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    article = models.BigIntegerField(null=False)
    title = models.TextField(null=False)
    availability = models.BooleanField()
    price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE, null=False)


class User(AbstractUser):
    pass


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    start_price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    alert_threshold = models.IntegerField(default=None)

    class Meta:
        unique_together = ('user', 'product')
