from serializers import AlbumSerializer
from rest_framework import generics
from music.models import Song,Album
class AlbumsView(generics.ListAPIView):
    serializer_class = AlbumSerializer
    def get_queryset(self):
        return Album.objects.all()