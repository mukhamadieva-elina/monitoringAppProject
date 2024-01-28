from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from monitoring.forms import LoginForm, RegistrationForm
from monitoring.models import User, EmailVerification


def index(request):
    return HttpResponse("INDEX")


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            is_verified = User.objects.filter(username=username, is_verified=True).exists()
            if user and is_verified:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            print("registration successful")
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm
    context = {'form': form}
    return render(request, 'registration.html', context)


def verification(request, **kwargs):
    if request.method == 'GET':
        verification_code = kwargs['verification_code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, verification_code=verification_code)
        if email_verification.exists():
            user.is_verified = True
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('index'))
