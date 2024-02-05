from django.urls import path

from monitoring import views

app_name = 'monitoring'
urlpatterns = [
    path('product/<int:article>', views.product, name='product')
]