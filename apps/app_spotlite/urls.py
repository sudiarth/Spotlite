from django.urls import path
from . import views

app_name = 'app_spotlite'

urlpatterns = [
    path('', views.index, name='index'),
]