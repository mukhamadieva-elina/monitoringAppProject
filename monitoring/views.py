from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from monitoring.forms import LoginForm, RegistrationForm, ProfileForm
from monitoring.models import User, EmailVerification, Product, UserProduct
from monitoring.wb_api_service import get_image, get_product_info


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
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


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


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'profile.html', context)


def wildberries(request):
    if request.method == 'POST':
        if get_product_info(request.POST['inputField']):
            Product.add_product(user=request.user, article=request.POST['inputField'], marketplace_name='Wildberries')
            return HttpResponseRedirect(reverse('wildberries'))
    products = UserProduct.get_user_products(request.user, 'Wildberries')
    product_form = []
    for product in products:
        product_form.append([product.title, get_image(product.article), product.price])
    context = {'products': product_form}
    return render(request, 'marketplace.html', context)
