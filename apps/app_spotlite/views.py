from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m
from django.db.models import Q
from django.db.models import Count, Sum

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from apps.auth_spotlite import models as um
import random, bcrypt, re

from apps.app_spotlite import lastfm_utilities as lastfm_utils

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

def index(request):
    if 'user_id' in request.session:
        context = {
            'songs': m.Song.objects.all().order_by('-created_at')[:24],
            'albums': m.Album.objects.all().order_by('-created_at')[:24],
            'artists': m.Artist.objects.all().order_by('-created_at')[:24],            
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'editors' : m.Editor.objects.filter(user_id=request.session['user_id']).order_by('-created_at'),
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/index.html', context)
        
    else:
        imagenr = random.randint(1,8)
        image = '/static/base_spotlite/img/bg{}.jpg'.format(imagenr)
        context = {
            'img_url' : image
        }
        return render(request, 'auth_spotlite/index.html', context)


def add_as_friend(request, following_id):
    if 'user_id' in request.session:
        follow = m.Follow()
        follow.follower_id = request.session['user_id']
        follow.following_id = following_id
        follow.save()
        # return redirect(request.META['HTTP_REFERER'])
        return redirect('app_spotlite:profile', following_id)

    return redirect('auth_spotlite:login')

def delete_as_friend(request, following_id):
    if 'user_id' in request.session:
        follow = m.Follow.objects.filter(following_id=following_id)
        follow.delete()
        # return redirect(request.META['HTTP_REFERER'])
        return redirect('app_spotlite:profile', user_id=following_id)
    return redirect('auth_spotlite:login')

def my_history(request):
    if 'user_id' in request.session:
        context = {
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/play_history.html', context)

    return redirect('auth_spotlite:login')

def my_musics(request, active):
    if 'user_id' in request.session:
        context = {
            'active': active,
            'albums': m.Album.objects.all()[:24],
            'artists': m.Artist.objects.all()[:24],      
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'likes' : m.Like.objects.filter(user_id=request.session['user_id']).order_by('-created_at'),
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/my_musics.html', context)
    
    return redirect('auth_spotlite:login')



def songs(request):
    context = {
        'songs' : m.Song.objects.all().order_by('-updated_at'),
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/songs.html', context)


def song(request, song_id):
    like = False
    like_check = m.Like.objects.filter(song_id=song_id, user_id=request.session['user_id'])
    if len(like_check) > 0:
        like = True

    context = {
        'albums': m.Album.objects.all()[:5],
        'artists': m.Artist.objects.all()[:5],
        'related_artist': m.Song.objects.filter(tags__song_id=song_id).distinct().values('artist_id'),
        'artists_grid': m.Artist.objects.all()[:12],
        'song' : m.Song.objects.get(id=song_id),
        'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
        'songs': m.Song.objects.annotate(total=Count('played_by')).order_by('-total')[:10], #POPULAR SONGS
        'like': like,
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/song.html', context)


def song_by_album(request, album_id):
    if 'user_id' in request.session:
        context = {
            'songs': m.Song.objects.filter(album_id=album_id)[:24],
            'album': m.Album.objects.get(id=album_id),          
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'editors' : m.Editor.objects.filter(user_id=request.session['user_id']),
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/songs_by_album.html', context)

    return redirect('auth_spotlite:login')


def song_by_artist(request, artist_id):
    if 'user_id' in request.session:
        context = {
            'songs': m.Song.objects.filter(artist_id=artist_id)[:24],
            'artist': m.Artist.objects.get(id=artist_id),          
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'editors' : m.Editor.objects.filter(user_id=request.session['user_id']),
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/songs_by_artist.html', context)

    return redirect('auth_spotlite:login')



def like_a_song(request, song_id):
    if 'user_id' in request.session:
        check = m.Like.objects.filter(user_id=request.session['user_id'], song_id=song_id)
        if len(check) == 0:
            like = m.Like()
            like.user_id = request.session['user_id']
            like.song_id = song_id
            like.save()

        return redirect('app_spotlite:index')

    return redirect('app_spotlite:profile')


def unlike_a_song(request, song_id):
    if 'user_id' in request.session:
        like = m.Like.objects.get(user_id=request.session['user_id'], song_id=song_id)
        like.delete()

        return redirect('app_spotlite:my_musics')

    return redirect('app_spotlite:profile')

def add_song_to_history(request, song_id):
    if 'user_id' in request.session:

        history = m.History()
        history.user_id = request.session['user_id']
        history.song_id = song_id
        
        check = m.History.objects.filter(user_id=request.session['user_id']).order_by('-created_at')[:1]

        if len(check) > 0:
            if check[0].song_id != song_id:
                history.save()
        else:
            history.save()

        # return redirect(request.META['HTTP_REFERER'])
        return redirect('app_spotlite:song', song_id=song_id)
    
    return redirect('auth_spotlite:login')


def add_to_playlist_step1(request, song_id):
    if 'user_id' in request.session:
        context = {
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'song_id': song_id,
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/playlists.html', context)

    return redirect('auth_spotlite:login')


def add_to_playlist_step2(request, song_id, playlist_id):
    if 'user_id' in request.session:
        if len(m.PlaylistItem.objects.filter(user_id=request.session['user_id'], song_id=song_id, playlist_id=playlist_id)) == 0:
            playlist_item = m.PlaylistItem()
            playlist_item.song_id = song_id
            playlist_item.playlist_id = playlist_id
            playlist_item.user_id = request.session['user_id']
            playlist_item.save()
        
        return redirect('app_spotlite:items_in_playlist', playlist_id=playlist_id)

    return redirect('auth_spotlite:login')


def playlists_editor(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            try:
                playlist = m.Playlist()
                playlist.title = request.POST['html_title']
                playlist.save()

                #save to editor
                editor = m.Editor()
                editor.playlist_id = playlist.id
                editor.user_id = request.session['user_id']
                editor.save()

                return redirect(request.META['HTTP_REFERER'])
            except:
                messages.error(request, 'invalid input')

        context = {
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'user_editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'can_add': True,
            'user': False,
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/playlists.html', context = context)

    return redirect('auth_spotlite:index')


def items_in_playlist(request, playlist_id):
    if 'user_id' in request.session:

        can_remove = False
        check_can_remove = m.Editor.objects.filter(playlist_id=playlist_id, user_id=request.session['user_id'])
        if len(check_can_remove) > 0:
            can_remove = True

        context = {
            # 'songs': m.Song.objects.filter(playlist_of__playlist_id=playlist_id),
            'items': m.PlaylistItem.objects.filter(playlist_id=playlist_id),
            'playlist': m.Playlist.objects.get(id=playlist_id),
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'editor_users': m.Editor.objects.filter(playlist_id=playlist_id),
            'can_remove': can_remove,
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
        }
        return render(request, 'app_spotlite/playlist-items.html', context = context)

    return redirect('auth_spotlite:login')


def delete_item_in_playlist(request, item_id):
    item = m.PlaylistItem.objects.get(id=item_id)
    item.delete()
    return redirect(request.META['HTTP_REFERER'])

def user_playlists(request, user_id):
    context = {
        'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
        'user_editors': m.Editor.objects.filter(user_id=user_id),
        'user': um.User.objects.get(id=user_id),
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }    
    return render(request, 'app_spotlite/playlists.html', context = context)


def like_playlist(request, playlist_id):
    if len(m.Editor.objects.filter(user_id=request.session['user_id'], playlist_id=playlist_id)) == 0:
        editor = m.Editor()
        editor.playlist_id = playlist_id
        editor.user_id = request.session['user_id']
        editor.save()
    
    return redirect(request.META['HTTP_REFERER'])

def delete_playlist(request, playlist_id):
    if len(m.Editor.objects.filter(playlist_id=playlist_id)) > 1:
        editor = m.Editor.objects.get(user_id=request.session['user_id'], playlist_id=playlist_id)
        editor.delete()
    else:
        playlist = m.Playlist.objects.get(id=playlist_id)
        playlist.delete()

    return redirect(request.META['HTTP_REFERER'])


def edit_playlist(request, playlist_id):
    playlist = m.Playlist.objects.get(id=playlist_id)

    if request.method == 'POST':
        playlist.title = request.POST['html_title']
        playlist.save()

        if request.POST['destination'] != '':
            return redirect(request.POST['destination'])
        else:
            return redirect('app_spotlite:profile')

    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
    else:
        referer = ''

    context = {
        'playlist': playlist,
        'destination': referer,
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    } 

    return render(request, 'app_spotlite/playlist-edit.html', context = context)

def profile(request, user_id):
    if 'user_id' in request.session:

        is_friend = False
        check_friend = m.Follow.objects.filter(following_id=user_id, follower_id=request.session['user_id'])
        if len(check_friend) > 0:
            is_friend = True

        following_people = []
        follower = m.Follow.objects.filter(follower_id=user_id)
        for follow in follower:
            following_people.append(follow.following_id)
       
        context = {
            'following' : following_people,
            'followers' : follower,
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'user': m.User.objects.get(id=user_id),
            'is_friend': is_friend,
            'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
            'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at'),
            'personal_histories' : m.History.objects.filter(user_id=request.session['user_id']).order_by('-created_at')[:8]
        }

        return render(request, 'app_spotlite/profile.html', context)
    return redirect('auth_spotlite:index')


def artist(request, artist_id):
    imagenr = random.randint(1,6)
    image = '/static/base_spotlite/img/artist{}.jpg'.format(imagenr)
    context = {
        'artist' : m.Artist.objects.get(id=artist_id),
        'img_url' : image,
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/profile-artist.html', context)

def settings(request):
    context = {  
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')  
    }
    return render(request, 'app_spotlite/settings.html', context)

def picture_upload(request, target):
    try:
        if request.method == 'POST' and request.FILES['file']:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            user = um.User.objects.get(id=request.session['user_id'])
            
            if target == "profile":
                user.profilepic = uploaded_file_url
            else:
                user.profilebackground = uploaded_file_url
            user.save()

            request.session['profilepic'] = user.profilepic
            request.session['profilebackground'] = user.profilebackground
    except:
        raise
        messages.error(request, 'Field can\'t be empty.')
        return redirect('app_spotlite:settings')
    return render(request, 'app_spotlite/settings.html')

def update_settings(request):
    if request.method == 'POST':
        try:
            errors = []
            user = um.User.objects.get(id=request.session['user_id'])
            
            email = request.POST['html_email']
            firstname = request.POST['html_firstname']
            surname = request.POST['html_surname']
            
            if len(email) == 0 or len(firstname) == 0 or len(surname) == 0:
                errors.append("Fields cannot be blank.")
                messages.error(request, "Fields cannot be blank.")
            if not EMAIL_REGEX.match(email):
                errors.append("Invalid e-mail.")    
                messages.error(request, "Invalid e-mail.")
            
            if request.POST['html_password'] == request.POST['html_confirm'] and len(request.POST['html_password']) > 0:
                password = request.POST['html_password']
                if password != request.POST['html_confirm']:
                    errors.append("Passwords do not match.")
                    messages.error(request, "Passwords do not match.")
                if len(password) < 6:
                    errors.append("Password must be longer than 6 characters.")
                    messages.error(request, "Password must be longer than 6 characters.")
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                user.password = hashed_password
            else:
                pass


            if len(errors) == 0:
                user.email = request.POST['html_email']
                user.firstname = request.POST['html_firstname']
                user.surname = request.POST['html_surname']

                request.session['user_id'] = user.id
                request.session['email'] = user.email
                request.session['firstname'] = user.firstname
                request.session['surname'] = user.surname
                user.save()
        except:
            raise
            print(errors)
    return redirect('app_spotlite:settings')

def change_membership(request):
    user = m.User.objects.get(id=request.session['user_id'])
    if user.premium == 0:
        user.premium = 1
    else:
        user.premium = 0
    request.session['premium'] = user.premium
    user.save()
    return redirect('app_spotlite:settings')

def post_search(request):
    search_keyword = request.POST['search_keyword']
    # return redirect('app_spotlite:search', search_keyword=search_keyword)
    return redirect('app_spotlite:search', search_keyword=search_keyword)

def search(request, search_keyword):
    context = {
        'search': True,
        'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
        'songs': m.Song.objects.filter(title__contains=search_keyword),
        'albums': m.Album.objects.filter(title__contains=search_keyword),
        'artists': m.Artist.objects.filter(name__contains=search_keyword),
        'users': um.User.objects.filter(Q(firstname__contains=search_keyword) | Q(surname__contains=search_keyword)),
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/search.html', context)

def presearch(request, search_keyword):
    context = {
        'artists': lastfm_utils.search_artist(search_keyword),
        'songs': lastfm_utils.search_song(search_keyword),
        'albums':  lastfm_utils.search_album(search_keyword),
        'histories' : m.History.objects.exclude(user_id=request.session['user_id']).order_by('-created_at')[:8],
        'friends' : m.Follow.objects.filter(follower_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/search.html', context)
