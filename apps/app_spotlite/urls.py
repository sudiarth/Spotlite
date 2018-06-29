from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app_spotlite'

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),

    path('picture_upload/<str:target>', views.picture_upload, name='picture_upload'),

    path('update_settings', views.update_settings, name='update_settings'),

    path('playlists-editor', views.playlists_editor, name='playlists_editor'),
    path('playlist/<int:playlist_id>/like', views.like_playlist, name='like_playlist'),
    
    path('playlist/<int:playlist_id>/delete', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/edit', views.edit_playlist, name='edit_playlist'),
    path('<int:user_id>/playlists', views.user_playlists, name='user_playlists'),
    path('play-history', views.my_history, name='my_history'),
    path('my-<active>', views.my_musics, name='my_musics'),

    path('playlist/<int:playlist_id>/items', views.items_in_playlist, name='items_in_playlist'),
    path('playlist/items/<int:item_id>/delete', views.delete_item_in_playlist, name='delete_item_in_playlist'),

    path('song/<int:song_id>/add-to-playlist', views.add_to_playlist_step1, name='add_to_playlist_step1'),
    path('song/<int:song_id>/add-to-playlist/<int:playlist_id>', views.add_to_playlist_step2, name='add_to_playlist_step2'),
    path('song/<int:song_id>', views.song, name='song'),

    path('album/<int:album_id>/songs', views.song_by_album, name='song_by_album'),
    path('artist/<int:artist_id>/songs', views.song_by_artist, name='song_by_artist'),

    path('song/<int:song_id>/add2history', views.add_song_to_history, name='add_song_to_history'),

    path('songs', views.songs, name='songs'),
    path('song/<int:song_id>/like', views.like_a_song, name='like_a_song'),
    path('song/<int:song_id>/unlike', views.unlike_a_song, name='unlike_a_song'),

    path('presearch/<str:search_keyword>/', views.presearch, name='presearch'),
    path('search/<str:search_keyword>/', views.search, name='search'),
    path('post_search/', views.post_search, name='post_search'),

    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('<int:user_id>/profile', views.profile, name='profile'),   

    path('user/<int:following_id>/follow', views.add_as_friend, name='add_as_friend'),
    path('user/<int:following_id>/unfollow', views.delete_as_friend, name='delete_as_friend'),

    path('change_membership', views.change_membership, name='change_membership'),

    path('', views.index, name='index'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
