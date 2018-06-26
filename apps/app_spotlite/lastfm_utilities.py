from django.shortcuts import render
import requests
import json
from pprint import pprint

from apps.app_spotlite import models as am

LASTFM_SEARCH_URL = "http://ws.audioscrobbler.com/2.0/?method={}.search&{}={}&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json"
#                   "http://ws.audioscrobbler.com/2.0/?method=artist.search&artist=cher&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json"
#                   http://ws.audioscrobbler.com/2.0/?method=album.search&album=believe&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json

LASTFM_GET_TRACK = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&mbid={}&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json"
LASTFM_GET_ALBUM = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&mbid={}&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json"
LASTFM_GET_ARTIST = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={}&api_key=756b9ac5c48cdf9d486133ec9e105440&format=json"

# UTILITIES
def get_request(url):
   response = requests.get(url)
   return json.loads(response.text)

def create_or_get_lastfm_artist(artist_data):
   try:
      artist = am.Artist.objects.get(mbid=artist_data['mbid'])
   except:
      artist = am.Artist()
      artist.lastfm_jsonparser(artist_data)
      artist.save()
   return artist

def create_or_get_lastfm_album(album_data):
   try:
      album = am.Artist.objects.get(mbid=album_data['mbid'])
   except:
      try:
         artist_response = get_request(LASTFM_GET_ARTIST.format(album_data['tracks']['track'][0]['artist']['mbid']))
         artist = create_or_get_lastfm_artist(artist_response['artist'])
         
         album = am.Album()
         album.lastfm_jsonparser(album_data)
         album.artist = artist
         album.save()
      except:
         album = None
   return album

def create_or_get_lastfm_song(song_data):
   try:
      song = am.Song.objects.get(mbid=song_data['mbid'])
   except:
      if len(song_data['album']['mbid']) > 0:
         album_response = get_request(LASTFM_GET_ALBUM.format(song_data['album']['mbid']))
         album = create_or_get_lastfm_album(album_response['album'])
         if album is not None:
            song = am.Song()
            song.lastfm_jsonparser(song_data)
            song.album = album
            song.save()

# FUNCIONS
def search_artist(method_name, entity_name, query):
   artists = []
   artist_url = LASTFM_SEARCH_URL.format(method_name, entity_name, query)
   data = get_request(artist_url)
   if 'results' in data:
      for artist_data in data['results']['artistmatches']['artist']:
         if len(artist_data['mbid']) > 0:
            artist = create_or_get_lastfm_artist(artist_data)
            artists.append(artist)
            print(artist_data['mbid'])
      return(artists)
# search_artist('artist', 'artist', '12034971098erhf012')

def search_album(method_name, entity_name, query):
   albums = []
   search_url = LASTFM_SEARCH_URL.format(method_name, entity_name, query)
   data = get_request(search_url)
   if 'results' in data:
      for alb in data['results']['albummatches']['album']:
         if len(alb['mbid']) > 0:
            album_data = get_request(LASTFM_GET_ALBUM.format(alb['mbid']))
            album = create_or_get_lastfm_album(album_data['album'])
            albums.append(album)
      return albums
search_album('album', 'album', '')

def search_song(method_name, entity_name, query):
   songs = []
   data = get_request(LASTFM_SEARCH_URL.format(method_name, entity_name, query))
   if 'results' in data:
      for sg in data['results']['trackmatches']['track']:
         if len(sg['mbid']) > 0:
            song_data = get_request(LASTFM_GET_TRACK.format(sg['mbid']))
            # pprint(song_data['track'])
            song = create_or_get_lastfm_song(song_data['track'])
            # songs.append(song)
      return songs
# search_song('track', 'track', 'yuhu')
