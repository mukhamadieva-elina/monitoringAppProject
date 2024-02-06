from django.urls import path

from monitoring import views

app_name = 'monitoring'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('wb/', views.wildberries, name='wildberries')
]
