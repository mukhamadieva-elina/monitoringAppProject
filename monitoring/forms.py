import uuid
from datetime import timedelta

from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm, UserCreationForm, UserChangeForm
from django import forms
from django.utils.timezone import now
from monitoring.models import User, EmailVerification


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=True)
        expired_at = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(verification_code=uuid.uuid4(), user=user, expired_at=expired_at)
        record.send_verification_email()
        return user


class ProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
