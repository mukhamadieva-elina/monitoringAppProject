from django.db import models


class Marketplace(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    article = models.BigIntegerField(null=False)
    title = models.TextField(null=False)
    availability = models.BooleanField()
    price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title
