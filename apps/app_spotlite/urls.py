from django.urls import path
from . import views

app_name = 'app_spotlite'

urlpatterns = [
    path('', views.index, name='index'),

    path('playlists-editor', views.playlists_editor, name='playlists_editor'),
    path('playlists', views.my_playlists, name='my_playlists'),
    path('playlist/<int:playlist_id>/like', views.like_playlist, name='like_playlist'),
    
    path('playlist/<int:playlist_id>/delete', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/edit', views.edit_playlist, name='edit_playlist'),
    path('<int:user_id>/playlists', views.user_playlists, name='user_playlists'),

    path('playlist/<int:playlist_id>/items', views.items_in_playlist, name='items_in_playlist'),
    path('playlist/items/<int:item_id>/delete', views.delete_item_in_playlist, name='delete_item_in_playlist'),

    path('song/<int:song_id>/add-to-playlist', views.add_to_playlist_step1, name='add_to_playlist_step1'),
    path('song/<int:song_id>/add-to-playlist/<int:playlist_id>', views.add_to_playlist_step2, name='add_to_playlist_step2'),    
]