from django.urls import path

from products import views

app_name = 'products'
urlpatterns = [
    path('product/<int:article>', views.product, name='product')
]
