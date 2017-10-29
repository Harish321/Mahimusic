from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm , PlaylistForm
from .models import Album, Song, Playlist
from django.http import HttpResponseRedirect
import os, sys
import shutil
def create_playlist(request):
    form = PlaylistForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['playlist_title']
            newPlaylist = Playlist(  playlist_title = title)
            newPlaylist.user = request.user
            newPlaylist.save()
            return HttpResponseRedirect('/')
    context = {'form':form}
    return render(request, 'music/createPlaylist.html', context)

def playlists(request):
    user_playlists=Playlist.objects.filter(user = request.user)
    context = {
        'user_playlists':user_playlists
    }
    return render(request,'music/playlists.html',context)

def playlist(request,playlist_id):
    currentPlaylist = Playlist(id = playlist_id,user = request.user)
    context = {
        'playlist':currentPlaylist
    }
    return render(request,'music/playlist.html',context)

def add_song_to_playlist(request,song_id,playlist_id):
    currentPlaylist = Playlist(id=playlist_id,user=request.user)
    currentSong = Song(id=song_id,user= request.user)
    currentPlaylist.playlist_songs.add(currentSong)

def add_album_to_playlist(request,album_id,playlist_id):
    songs = Song.objects.filter(id=album_id,user=request.user)
    for song in songs:
        add_song_to_playlist(request,song.id,playlist_id)
    return HttpResponseRedirect('/')

def add_songs_to_playlist(request,playlist_id):
    if request.method == "POST":
        songs_id = request.POST.getlist('songid[]')
        for song_id in songs_id:
            add_song_to_playlist(request,song_id,playlist_id)
        return HttpResponseRedirect('/')
    songs = Song.objects.filter(user=request.user).exclude(playlist__id__exact=playlist_id)
    playlist = Playlist.objects.filter(id = playlist_id)
    context = {
        'songs':songs,
        'playlist' : playlist[0]
    }
    return render(request,'music/addsongstoplaylist.html',context)
