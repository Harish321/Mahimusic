from music.models import Song,Album
from rest_framework import serializers
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'song_title',
            'album',
            'audio_file'
        ]

class AlbumSerializer(serializers.ModelSerializer):
    class Meta():
        model = Album
        fields = [
            'id',
            'album_title',
            'album_logo'
        ]

class SongUrlSerializer(serializers.ModelSerializer):
    class  Meta():
        model = Song
        fields = ['audio_file']