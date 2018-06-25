from django.shortcuts import render, redirect
from django.contrib import messages
from . import models as m
import apps.auth_spotlite.models as mu
from pprint import pprint
# from django.db.models import Q


def index(request):
    return render(request, 'app_spotlite/index.html')


def my_playlists(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            try:
                playlist = m.Playlist()
                playlist.content = request.POST['html_content']
                playlist.user_id = request.session['user_id']
                playlist.save()
                return redirect(request.META['HTTP_REFERER'])
            except:
                messages.error(request, 'invalid input')

        is_friends = []
        for playlist in playlists_by_user(request, request.session['user_id']):
            is_friends.append({'playlist_id': playlist.id, 'is_friend': is_friend(request, playlist.user_id) })
        
        context = {
            'playlists': playlists_by_user(request, request.session['user_id']),
            'is_friends': is_friends
        }
        return render(request, 'myface/playlists.html', context = context)

    return redirect('auth_spotlite:index')


def user_playlists(request, user_id):
    is_friends = []
    for playlist in playlists_by_user(request, user_id):
        is_friends.append({'playlist_id': playlist.id, 'is_friend': is_friend(request, playlist.user_id) })
                
    context = {
        'playlists': playlists_by_user(request, user_id),
        'user': mu.User.objects.get(id=user_id),
        'is_friends': is_friends
    }    
    return render(request, 'myface/playlists.html', context = context)


def playlists_by_user(request, user_id):
    return m.Playlist.objects.filter(user_id=user_id).order_by('-created_at')


def delete_playlist(request, playlist_id):
    playlist = m.Playlist.objects.get(id=playlist_id)
    playlist.delete()
    return redirect(request.META['HTTP_REFERER'])


def edit_playlist(request, playlist_id):
    playlist = m.Playlist.objects.get(id=playlist_id)

    if request.method == 'POST':
        playlist.content = request.POST['html_content']
        playlist.save()
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'playlist': playlist
    } 

    return render(request, 'myface/edit.html', context = context)
    