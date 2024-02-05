"""
URL configuration for monitoringAppProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from monitoring import views
from monitoring.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('monitoring/', include('monitoring.urls', namespace='monitoring')),
    path('verification/<str:email>/<uuid:verification_code>/', views.verification, name='verification'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('wb/', views.wildberries, name='wildberries')
]
