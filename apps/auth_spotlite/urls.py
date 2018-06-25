from django.urls import path
from . import views

app_name = 'auth_spotlite'

urlpatterns = [
    
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('authenticate/<str:action>', views.authenticate, name='authenticate'),

    path('', views.index, name='index'),
]