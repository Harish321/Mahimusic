from django.conf.urls import include, url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/$', views.songs, name='songs'),
    #url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^create_playlist/$',views.create_playlist, name = 'create_playlist'),
    url(r'^playlists/$',views.playlists,name = 'playlists'),
    url(r'^playlist/(?P<playlist_id>[0-9]+)/$',views.playlist,name='playlist'),
    url(r'^addsongtoplaylist/(?P<song_id>[0-9]+)/(?P<playlist_id>[0-9]+)',views.add_song_to_playlist,name='addsongtoplaylist'),
    url(r'^addalbumtoplaylist/(?P<album_id>[0-9]+)/(?P<playlist_id>[0-9]+)',views.add_album_to_playlist,name='addalbumtoplaylist'),
    url(r'^addsongstoplaylist/(?P<playlist_id>[0-9]+)',views.add_songs_to_playlist,name='addsongstoplaylist'),
    url(r'^deletesongfromplaylist/(?P<playlist_id>[0-9]+)/(?P<song_id>[0-9]+)',views.delete_song_from_playlist,name='deletesongfromplaylist'),
    url(r'^addalbumstoplaylist/(?P<playlist_id>[0-9]+)',views.add_albums_to_playlist,name='addalbumstoplaylist'),
    url(r'^deleteplaylist/(?P<playlist_id>[0-9]+)',views.delete_playlist,name = 'deleteplaylist'),
    url(r'^removeallsongsfromplaylist/(?P<playlist_id>[0-9]+)/(?P<typ>[0-9]+)',views.remove_allsongs_from_playlist,name = 'removeallsongsfromplaylist'),
    url(r'^renameplaylist/(?P<playlist_id>[0-9]+)',views.rename_playlist,name='rename_playlist'),
    url(r'^users/',views.users,name='users'),
    url(r'^viewuser/(?P<user_id>[0-9]+)',views.view_user,name = 'viewuser' ),
    url(r'^index2',views.index2,name='index2'),
    url(r'^search',views.search,name ='search'),
    url(r'^addalbums',views.addAlbums,name = 'addalbums'),
    url(r'^addgivenalbum/(?P<album_id>[0-9]+)',views.addGivenAlbum,name='addgivenalbum'),
    url(r'^myalbums',views.myAlbums,name = "myalbums"),
    url(r'^removegivenalbum/(?P<album_id>[0-9]+)',views.removeGivenAlbum,name="removegivenalbum")
]
