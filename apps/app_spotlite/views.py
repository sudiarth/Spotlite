from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m
import apps.auth_spotlite.models as mu
from pprint import pprint
# from django.db.models import Q


def index(request):
    return render(request, 'app_spotlite/index.html')

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
        'user': mu.User.objects.get(id=user_id),
    }    
    return render(request, 'app_spotlite/playlists.html', context = context)


# def playlists_by_user(request, user_id):
#     return m.Playlist.objects.filter(user_id=user_id).order_by('-created_at')

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
    