from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m
# from django.db.models import Q

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from apps.auth_spotlite import models as um
import random


def index(request):
    if 'user_id' in request.session:
        return render(request, 'app_spotlite/index.html')
    else:
        imagenr = random.randint(1,8)
        image = '/static/base_spotlite/img/bg{}.jpg'.format(imagenr)
        context = {
            'img_url' : image
        }
        return render(request, 'auth_spotlite/index.html', context)


def play_history(request):
    context = {
        'histories' : m.History.objects.filter(user_id=request.session['user_id']).order_by('-created_at')
    }
    return render(request, 'app_spotlite/play_history.html', context)


def songs(request):
    context = {
        'songs' : m.Song.objects.all().order_by('-updated_at')
    }
    return render(request, 'app_spotlite/songs.html', context)


def song(request, song_id):
    context = {
        'song' : m.Song.objects.get(id=song_id)
    }
    return render(request, 'app_spotlite/song.html', context)


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
    
    return redirect('app_spotlite:index')


def add_to_playlist_step1(request, song_id):
    if 'user_id' in request.session:
        context = {
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'song_id': song_id
        }
        return render(request, 'app_spotlite/playlists.html', context)

    return redirect('app_spotlite:index')


def add_to_playlist_step2(request, song_id, playlist_id):
    if 'user_id' in request.session:
        if len(m.PlaylistItem.objects.filter(user_id=request.session['user_id'], song_id=song_id, playlist_id=playlist_id)) == 0:
            playlist_item = m.PlaylistItem()
            playlist_item.song_id = song_id
            playlist_item.playlist_id = playlist_id
            playlist_item.user_id = request.session['user_id']
            playlist_item.save()
        
        return redirect('app_spotlite:my_playlists')

    return redirect('app_spotlite:index')


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
            'can_add': True,
            'user': False
        }
        return render(request, 'app_spotlite/playlists.html', context = context)

    return redirect('auth_spotlite:index')


def my_playlists(request):

    if 'user_id' in request.session:
        context = {
            'editors': m.Editor.objects.filter(user_id=request.session['user_id']),
            'user': False
        }
        return render(request, 'app_spotlite/playlists.html', context = context)

    return redirect('auth_spotlite:index')


def items_in_playlist(request, playlist_id):
    if 'user_id' in request.session:

        context = {
            'items': m.PlaylistItem.objects.filter(playlist_id=playlist_id),
            'playlist': m.Playlist.objects.get(id=playlist_id),
            'editors': m.Editor.objects.filter(playlist_id=playlist_id)
        }
        return render(request, 'app_spotlite/playlist-items.html', context = context)

    return redirect('app_spotlite:index')


def delete_item_in_playlist(request, item_id):
    item = m.PlaylistItem.objects.get(id=item_id)
    item.delete()
    return redirect(request.META['HTTP_REFERER'])

def user_playlists(request, user_id):

    context = {
        'editors': m.Editor.objects.filter(user_id=user_id),
        'user': um.User.objects.get(id=user_id),
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
            return redirect('app_spotlite:my_playlists')

    if 'HTTP_REFERER' in request.META:
        referer = request.META['HTTP_REFERER']
    else:
        referer = ''

    context = {
        'playlist': playlist,
        'destination': referer
    } 

    return render(request, 'app_spotlite/playlist-edit.html', context = context)


def spotify(request):
    return render(request, 'app_spotlite/spotify.html')

def profile(request):
    return render(request, 'app_spotlite/profile.html')

def settings(request):
    return render(request, 'app_spotlite/settings.html')

def picture_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        user = um.User.objects.get(id=request.session['user_id'])
        user.profilepic = uploaded_file_url
        user.save()

        request.session['profilepic'] = user.profilepic
        return redirect('app_spotlite:profile')
    return render(request, 'app_spotlite/profile.html')

def update_settings(request):
    user = um.User.objects.get(id=request.session['user_id'])
    user.email = request.POST['html_email']
    user.firstname = request.POST['html_firstname']
    user.surname = request.POST['html_surname']
    user.save()
    request.session['user_id'] = user.id
    request.session['email'] = user.email
    request.session['firstname'] = user.firstname
    request.session['surname'] = user.surname
    return redirect('app_spotlite:settings')


def update_password(request):
    user = um.User.objects.get(id=request.session['user_id'])
    if request.POST['html_password'] == request.POST['html_confirm'] and len(request.POST['html_password']) > 0:
        user.password = request.POST['html_password']
        user.save()
    return redirect('app_spotlite:settings') 
    