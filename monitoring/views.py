from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from marketplaces.wildberries.wildberries import Wildberries
from monitoring.forms import LoginForm, RegistrationForm, ProfileForm
from monitoring.models import User, EmailVerification, UserProduct


def index(request):
    context = {}
    return render(request, 'index.html', context)


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
                return HttpResponseRedirect(reverse('monitoring:index'))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('monitoring:index'))


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('monitoring:index'))
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
            return HttpResponseRedirect(reverse('monitoring:login'))
        else:
            return HttpResponseRedirect(reverse('monitoring:index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('monitoring:profile'))
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'profile.html', context)


# TODO изменить контроллер так, чтобы работал с любым маркетплейсом
def wildberries(request):
    if request.method == 'POST':
        if Wildberries.get_product_info(request.POST['inputField']):
            UserProduct.add_product(user=request.user, article=request.POST['inputField'],
                                    marketplace_name='Wildberries')
            return HttpResponseRedirect(reverse('monitoring:wildberries'))
    products = UserProduct.get_user_products(request.user, 'Wildberries')
    product_form = []
    for product in products:
        product_url = reverse('products:product', kwargs={'article': product.article})
        product_link = f'{settings.DOMAIN_NAME}{product_url}'
        product_form.append([product.title, Wildberries.get_image(product.article), product.price, product_link])
    context = {'products': product_form}
    return render(request, 'marketplace.html', context)
