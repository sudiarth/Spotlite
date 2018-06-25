from django.urls import path
from . import views

app_name = 'app_spotlite'

urlpatterns = [
    path('', views.index, name='index'),

    path('playlists', views.my_playlists, name='my_playlists'),
    path('playlist/<int:playlist_id>/delete', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/edit', views.edit_playlist, name='edit_playlist'),
    path('<int:user_id>/playlists', views.user_playlists, name='user_playlists'),    
]