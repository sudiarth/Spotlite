from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app_spotlite'

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('picture_upload', views.picture_upload, name='picture_upload'),

    path('update_settings', views.update_settings, name='update_settings'),
    path('update_password', views.update_password, name='update_password'),

    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)