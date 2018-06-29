import json, requests, sys, youtube_dl, os
from . import models as m
from pprint import pprint

# YOUTUBE API
YOUTUBE_API_KEY = "AIzaSyBmBlP0RO2Whz4BUgduujf_T0fHRKAe2xc"
YOUTUBE_SEARCH_URL = "https://content.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={}"

# YOUTUBE DOWNLOADER
ydl_opts = {
      'outtmpl': '/home/nawi/Desktop/Spotlite/media/audio/%(title)s-%(id)s.%(ext)s',
      'format': 'bestaudio/best',
      'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
      }],
}

# SUPPORTING UTILITIES
def get_request(url):
   response = requests.get(url)
   return json.loads(response.text)

def get_youtube_url(keyword, song_id):
   videos = []
   response = get_request(YOUTUBE_SEARCH_URL.format(keyword, YOUTUBE_API_KEY))
   try:
      video_id = response['items'][0]['id']['videoId']
      videos = [YOUTUBE_WATCH_URL.format(video_id)]

      # pprint(response['items'][0]['snippet']['title']+'-'+video_id+'.mp3')

      songs = []

      song = m.Song.objects.get(id=song_id)
      song.mp3url = '/media/audio/'+response['items'][0]['snippet']['title']+'-'+video_id+'.mp3'
      song.save()

      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(videos)

   except:
      pass
