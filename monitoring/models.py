from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Marketplace(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    article = models.BigIntegerField(null=False)
    title = models.TextField(null=False)
    availability = models.BooleanField()
    price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE, null=False)


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=False)
    is_verified = models.BooleanField(default=False)


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    start_price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    alert_threshold = models.IntegerField(default=None)

    class Meta:
        unique_together = ('user', 'product')


class EmailVerification(models.Model):
    verification_code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification for user: {self.user.email}'

    def send_verification_email(self):
        link = reverse('verification', kwargs={'email': self.user.email, 'verification_code': self.verification_code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = 'Verification'
        message = f'Your verification link {verification_link}'
        print("before sending the message")
        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [self.user.email],
                  fail_silently=False,
                  )

    def is_expired(self):
        return now() >= self.expired_at
