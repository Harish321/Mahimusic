from django import forms
from django.contrib.auth.models import User

from .models import Album, Song, Playlist


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.Form):
    audio_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True, 'onchange': 'this.form.submit();'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PlaylistForm(forms.ModelForm):
	class Meta:
		model = Playlist
		fields = ['playlist_title']

#form to rename playlist
class RenamePlaylistForm(forms.Form):
    new_playlist_title = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))