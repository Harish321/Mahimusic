from django.conf.urls import url
from views import AlbumsView
urlpatterns = [
    url(r'^albums/', AlbumsView.as_view(), name='albumsview'),
]