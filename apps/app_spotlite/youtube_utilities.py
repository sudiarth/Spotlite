import json, requests
from pprint import pprint

YOUTUBE_API_KEY = "AIzaSyBmBlP0RO2Whz4BUgduujf_T0fHRKAe2xc"
YOUTUBE_SEARCH_URL = "https://content.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}"

YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={}"

# SUPPORTING UTILITIES
def get_request(url):
   response = requests.get(url)
   return json.loads(response.text)

def get_youtube_url(keyword):
   response = get_request(SEARCH_URL.format(keyword, API_KEY))
   # pprint(response)
   video_id = response['items'][0]['id']['videoId']
   print(YOUTUBE_WATCH_URL.format(video_id))
# get_youtube_url('madonna american girl')
