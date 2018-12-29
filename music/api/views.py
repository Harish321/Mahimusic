from .serializers import AlbumSerializer,SongSerializer,SongUrlSerializer
from rest_framework import generics
from music.models import Song,Album
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class AlbumsView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    def get_queryset(self):
        return Album.objects.all()
class AlbumView(generics.RetrieveAPIView):
    serializer_class = AlbumSerializer
    def get_queryset(self):
        return  Album.objects.all()
class SongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    def get_queryset(self):
        return Song.objects.filter(album=self.kwargs['album_id'])
class SongsUrlView(generics.ListAPIView):
    serializer_class = SongUrlSerializer
    def get_queryset(self):
        return Song.objects.filter(album=self.kwargs['album_id'])