from django.conf.urls import url
from .views import AlbumsView,SongsView,AlbumView,SongsUrlView
urlpatterns = [
    url(r'^albums/$', AlbumsView.as_view(), name='albumsview'),
    url(r'^songs/(?P<album_id>[0-9]+)',SongsView.as_view(),name='songsview'),
    url(r'^songsurl/(?P<album_id>[0-9]+)',SongsUrlView.as_view(),name='songsview'),
    url(r'^album/(?P<pk>[0-9]+)/$', AlbumView.as_view(), name='albumsview'),
    
]