from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from monitoring.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


# TODO
#class RegisterForm(UserCreationForm):
#    class Meta:
#        model = User
#        fields = ('username', 'email')
