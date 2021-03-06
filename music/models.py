from django.contrib.auth.models import Permission, User
from django.db import models
import os


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist

#For every song uploaded there will be a specific path like user/album/file.mp3
def get_upload_path(instance, filename):
    #if not os.path.exists(str(instance.user.pk)+'/'+str(instance.album.album_title)):
    #    os.makedirs(str(instance.user.pk)+'/'+str(instance.album.album_title))
    return str(instance.user.pk)+'/'+str(instance.album.album_title)+'/'+str(instance.song_title)+'.mp3'

class Song(models.Model):
    user = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

'''
    This models is for playlists and stores songs
'''
class Playlist(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    playlist_title  = models.CharField(max_length=10)
    playlist_songs = models.ManyToManyField(Song)

'''
    This model is for user and his album interests
'''
class UserAlbum(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, default = 1, on_delete=models.CASCADE) 

