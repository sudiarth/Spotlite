from django.shortcuts import render
import requests
import json
from pprint import pprint

from apps.app_spotlite import models as am
from apps.app_spotlite import youtube_utilities as youtube_utils

API_KEY = "756b9ac5c48cdf9d486133ec9e105440"
LASTFM_SEARCH_URL = "http://ws.audioscrobbler.com/2.0/?method={}.search&{}={}&api_key={}&format=json"

LASTFM_GET_TRACK = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&mbid={}&api_key={}&format=json"
LASTFM_GET_ALBUM = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&mbid={}&api_key={}&format=json"
LASTFM_GET_ARTIST = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={}&api_key={}&format=json"

# UTILITIES
def get_request(url):
   response = requests.get(url)
   return json.loads(response.text)

def create_or_get_lastfm_artist_by_mbid(mbid):
   try:
      artist = am.Artist.objects.get(mbid=mbid)
   except:
      try:
         response = get_request(LASTFM_GET_ARTIST.format(mbid, API_KEY))
         artist = am.Artist()
         artist.lastfm_jsonparser(response['artist'])
         artist.save()
      except:
         artist = None
   return artist

def create_or_get_lastfm_album_by_mbid(mbid):
   try:
      album = am.Artist.objects.get(mbid=mbid)
   except:
      try:
         response = get_request(LASTFM_GET_ALBUM.format(mbid, API_KEY))
         artist = create_or_get_lastfm_artist_by_mbid(response['album']['tracks']['track'][0]['artist']['mbid'])

         album = am.Album()
         album.lastfm_jsonparser(response['album'])
         album.artist = artist
         album.save()
      except:
         album = None
   return album

def create_or_get_lastfm_song_by_mbid(mbid):
   # song = None
   try:
      song = am.Song.objects.get(mbid=mbid)
   except:
      try:
         data = get_request(LASTFM_GET_TRACK.format(mbid, API_KEY))
         song = am.Song()
         song.lastfm_jsonparser(data['track'])
         song.album = create_or_get_lastfm_album_by_mbid(data['track']['album']['mbid'])
         song.artist = create_or_get_lastfm_artist_by_mbid(data['track']['artist']['mbid'])
         song.save()
      except:
         song = None
   return song



# SEARCH FUNCIONS
def search_artist(query):
   artists = []
   search_url = LASTFM_SEARCH_URL.format('artist', 'artist', query, API_KEY)
   data = get_request(search_url)
   if 'results' in data:
      for artist_data in data['results']['artistmatches']['artist']:
         if len(artist_data['mbid']) > 0:
            artist = create_or_get_lastfm_artist_by_mbid(artist_data['mbid'])
            if artist is not None:
               artists.append(artist)
               print(artist.mbid)
      return(artists)
# search_artist('blink')

def search_album(query):
   albums = []
   search_url = LASTFM_SEARCH_URL.format('album', 'album', query, API_KEY)
   data = get_request(search_url)
   if 'results' in data:
      for alb in data['results']['albummatches']['album']:
         if len(alb['mbid']) > 0:
            album = create_or_get_lastfm_album_by_mbid(alb['mbid'])
            if album is not None:
               print(album.title)
               albums.append(album)
   return albums
# search_album('pilot')

def search_song(query):
   songs = []
   data = get_request(LASTFM_SEARCH_URL.format('track', 'track', query, API_KEY))
   if 'results' in data:
      for sg in data['results']['trackmatches']['track']:
         if 'mbid' in sg: 
            if len(sg['mbid']) > 0:
               song = create_or_get_lastfm_song_by_mbid(sg['mbid'])
               if song is not None:
                  songs.append(song)
                  print('{} - {}'.format(song.title, song.album.artist.name))
                  # print(youtube_utils.get_youtube_url(song.title)
   return songs
search_song('super')
