import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from monitoring.models import EmailVerification, User


@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expired_at = now() + timedelta(hours=24)
    record = EmailVerification.objects.create(verification_code=uuid.uuid4(), user=user, expired_at=expired_at)
    record.send_verification_email()
