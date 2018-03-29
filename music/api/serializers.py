from music.models import Song,Album
from rest_framework import serializers
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'song_title',
            'album'
        ]

class AlbumSerializer(serializers.ModelSerializer):
    class Meta():
        model = Album
        fields = [
            'album_title',
            'album_logo'
        ]