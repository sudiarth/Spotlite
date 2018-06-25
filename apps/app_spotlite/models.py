from django.db import models


class User(models.Model):
   email = models.CharField(max_length=64, unique=True)
   firstname = models.CharField(max_length=32)
   surname = models.CharField(max_length=32)
   password = models.CharField(max_length=32)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
   following = models.ForeignKey(User, related_name='following_by', on_delete=models.CASCADE)
   follower = models.ForeignKey(User, related_name='follower_of', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Label(models.Model):
   name = models.CharField(max_length=32)
   description = models.TextField()
   logo = models.CharField(max_length=64)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Artist(models.Model):
   name = models.CharField(max_length=32)
   photo = models.CharField(max_length=64)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Album(models.Model):
   title = models.CharField(max_length=32)
   cover = models.CharField(max_length=64)

   artist = models.ForeignKey(Artist, related_name='artists', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Song(models.Model):
   title = models.CharField(max_length=32)
   genre = models.CharField(max_length=32)
   text = models.TextField()
   cover = models.CharField(max_length=32)

   album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Playlist(models.Model):
   title = models.CharField(max_length=32)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Editor(models.Model):
   user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
   playlist = models.ForeignKey(Playlist, related_name='editors', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class PlaylistItem(models.Model):
   song = models.ForeignKey(Song, related_name='playlist_of', on_delete=models.CASCADE)
   playlist = models.ForeignKey(Playlist, related_name='playlist_items', on_delete=models.CASCADE)
   user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class History(models.Model):
   user = models.ForeignKey(User, related_name='plays', on_delete=models.CASCADE)
   song = models.ForeignKey(Song, related_name='played_by', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
   user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
   song = models.ForeignKey(Song, related_name='like_by', on_delete=models.CASCADE)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)