from django.urls import path
from . import views

app_name = 'app_spotlite'

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('', views.index, name='index'),
]