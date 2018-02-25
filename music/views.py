from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm , PlaylistForm, RenamePlaylistForm
from .models import Album, Song, Playlist, User
from django.http import HttpResponseRedirect
import os, sys
import shutil
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
from mutagen import *
'''def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


files variable stores all the uploaded files.

'''
def create_song(request):
    form = SongForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        files = request.FILES.getlist('audio_file')
        for a in files:
            file = File(a)
            
            ''' IF the uploaded file contains any title in its tag then it takes that else it takes the uploaded file name''' 
            file_name = ''
            if 'TIT2' in file:
                if os.name =='nt':
                    file_name= str(file.tags['TIT2']).replace(":","")
                    file_name= file_name.replace(">","")
                    file_name= file_name.replace("<","")
                    file_name= file_name.replace("/","")
                    file_name= file_name.replace("-","")
                else:
                    file_name = file.tags['TIT2']
            else:
                file_name = a.name

            '''IF there isn't any data about album in the mp3 it sets it to unknown'''
            file_album_name=''
            if 'TALB' in file:
                
                file_album_name=file.tags['TALB']
            else:
                file_album_name='Unknown'
            
            '''If album is created for the first time'''
            if not Album.objects.filter(album_title=file_album_name,user=request.user):
                '''
                The below if condition takes care of first time upload
                i.e
                If there is no folder for the new user then it creates one
                '''

                if not os.path.exists('media/'+str(request.user.pk)):
                    os.makedirs('media/'+str(request.user.pk))
            

                '''new folder for the album is created'''
                if not os.path.exists(('media/'+str(request.user.pk)+'/'+str(file_album_name))):
                    os.makedirs('media/'+str(request.user.pk)+'/'+str(file_album_name))
            

                '''creates a thumbnail for the album'''
                filename='default.jpg'#default image
                if 'APIC:' in file:
                    artwork = file.tags['APIC:'].data
                    filename='media/'+str(request.user.pk)+'/'+str(file_album_name)+'/'+str(file_album_name)+'.jpg'
                    with open(filename, 'wb+') as img:
                        img.write(artwork) # write artwork to new image
                        
                    statinfo = os.stat(filename)#gives details of the image
                    if statinfo.st_size==0:
                        '''If there is no image then we use default'''
                        filename='default.jpg'
                    else:
                        '''The below file name stores address .../..../media/filename'''
                        filename=str(request.user.pk)+'/'+str(file_album_name)+'/'+str(file_album_name)+'.jpg'

                new=Album(album_title=file_album_name,user=request.user,album_logo=filename)
                new.save()
                '''If the album exists then below else statement checks if the uploaded is duplicate song or not'''
            else:
                if Song.objects.filter(user=request.user,album__album_title=file_album_name,song_title=file_name):
                    context = {
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/create_song.html', context)
            
            '''save the uploaded files to the file system and insert into database'''
            song_title=file_name
            with open(str("media/"+str(request.user.pk)+"/"+str(file_album_name)+"/"+str(song_title)+".mp3"), 'wb+') as destination:
                for chunk in a.chunks():
                    destination.write(chunk)
            upload_url = str(request.user.pk)+"/"+str(file_album_name)+"/"+str(song_title)+".mp3"
            new_song = Song(user = request.user, album = Album.objects.get(album_title=file_album_name,user=request.user), song_title = song_title, audio_file = upload_url)
            new_song.save()
            
        return HttpResponseRedirect('/') #redirects to the home page
    context = {
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id,user=request.user)
    shutil.rmtree('media/'+str(request.user.id)+'/'+str(album.album_title))#deletes folder
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return HttpResponseRedirect('/')



'''
    if the folder is deleted then redirect to home page
'''
def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id,user=request.user)
    song.delete()
    remove_song(request.user.pk,album.album_title,song.song_title)
    deleted = if_no_songs_delete_folder(request.user.pk,album.album_title,album)
    if deleted:
        return HttpResponseRedirect('/')
    return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        l=[]
        try:
            album = get_object_or_404(Album, pk=album_id,user = user)
            allsongs  = Song.objects.filter(user=request.user,album=album_id)
            for a in allsongs:
                l.append(a.audio_file.url)

        except:
            #if the requested album is not uploaded by the user then it redirects to the album page 
            #without delete options
            album = get_object_or_404(Album,pk=album_id)
            albumUser = album.user
            allsongs = Song.objects.filter(user=albumUser,album=album_id)
            for a in allsongs:
                l.append(a.audio_file.url)
            return render(request, 'music/detail.html', {'album': album, 'user': user, 'l':l, 'albumUser':albumUser})
        return render(request, 'music/detail.html', {'album': album, 'user': user, 'l':l})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        allsongs  = Song.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = allsongs.filter(
                Q(song_title__icontains=query)
            ).distinct()
            l = []
            l = givesongsurl(song_results)
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
                'l':l,
                'searched':False
            })
        else:
            l = []
            for a in allsongs:
                l.append(a.audio_file.url)
            return render(request, 'music/index.html', {'albums': albums,'l':l, 'searched':False})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/music/')
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    
    return render(request, 'music/login.html')

def givesongsurl(allsongs):
    l=[]
    for a in allsongs:
        l.append(a.audio_file.url)
    return l

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            l = givesongsurl(users_songs)
            
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'l':l
        })

'''
    if there is no mp3 file then it deletes the album and returns True. 
    if there is a mp3 file it does nothing
'''
def if_no_songs_delete_folder(usrid,albtitle,albm):
    for file in os.listdir('media/'+str(usrid)+'/'+str(albtitle)):
        if file.endswith(".mp3"):
            break
    else:
        shutil.rmtree('media/'+str(usrid)+'/'+str(albtitle))
        albm.delete()
        return True
    return False

def remove_song(usrid,albtitle,sngtitle):
    os.remove('media/'+str(usrid)+'/'+str(albtitle)+'/'+str(sngtitle)+'.mp3')
    return

def create_playlist(request):
    form = PlaylistForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['playlist_title']
            if len(Playlist.objects.filter(playlist_title = title , user = request.user))==0:
                newPlaylist = Playlist(  playlist_title = title)
                newPlaylist.user = request.user
                newPlaylist.save()
                return redirect('/music/playlist/'+str(newPlaylist.id))
            else :
                context = {
                    'form':form,
                    'error':'playlist exists'
                }
                return render(request, 'music/createPlaylist.html', context)            
    context = {'form':form}
    return render(request, 'music/createPlaylist.html', context)

def playlists(request):
    user_playlists=Playlist.objects.filter(user = request.user)
    songs_in_playlist = []
    for this in user_playlists:
        songs = this.playlist_songs.all()
        songs_in_playlist.append(givesongsurl(songs))
    l=[]
    zipped = zip(user_playlists,songs_in_playlist)
    context = {
        'user_playlists':user_playlists,
        'songs_in_playlist':songs_in_playlist,
        'l':l,
        'zipped':zipped,
    }
    return render(request,'music/playlists.html',context)

def playlist(request,playlist_id):
    currentPlaylist = Playlist.objects.filter(id = playlist_id,user = request.user)[0]
    allsongs = currentPlaylist.playlist_songs.all()
    l = givesongsurl(allsongs)
    context = {
        'playlist':currentPlaylist,
        'l':l
    }
    return render(request,'music/playlist.html',context)

def delete_playlist(request,playlist_id):
    Playlist(id = playlist_id).delete()
    return redirect('/music/playlists')
    

def add_song_to_playlist(request,song_id,playlist_id):
    currentPlaylist = Playlist(id=playlist_id,user=request.user)
    currentSong = Song(id=song_id,user= request.user)
    if currentSong not in currentPlaylist.playlist_songs.all():
        currentPlaylist.playlist_songs.add(currentSong)

def delete_song_from_playlist(request,playlist_id,song_id):
    song = Song(id = song_id)
    playlist = Playlist(id = playlist_id)
    playlist.playlist_songs.remove(song)
    return redirect('/music/playlist/'+playlist_id)

def remove_allsongs_from_playlist(request,playlist_id,typ):
    currenturl = request.get_full_path()
    songs = Song.objects.filter(user=request.user,playlist__id= playlist_id)
    for song in songs:
        delete_song_from_playlist(request,playlist_id,song.id)
    if int(typ)==0:
        return redirect('/music/playlist/'+playlist_id)
    return redirect('/music/playlists')

def add_album_to_playlist(request,album_id,playlist_id):
    songs = Song.objects.filter(album_id=album_id,user=request.user)
    for song in songs:
        add_song_to_playlist(request,song.id,playlist_id)

def add_songs_to_playlist(request,playlist_id):
    if request.method == "POST":
        songs_id = request.POST.getlist('songid[]')
        for song_id in songs_id:
            add_song_to_playlist(request,song_id,playlist_id)
        return redirect('/music/playlist/'+playlist_id)
    songs = Song.objects.filter(user=request.user).exclude(playlist__id__exact=playlist_id)
    playlist = Playlist.objects.get(id = playlist_id)
    l=[]
    context = {
        'songs':songs,
        'playlist' : playlist,
        'l':l
    }
    return render(request,'music/addsongstoplaylist.html',context)

def add_albums_to_playlist(request,playlist_id):
    if request.method == "POST":
        albums_id = request.POST.getlist('albumid[]')
        for album_id in albums_id:
            add_album_to_playlist(request,album_id,playlist_id)
        return redirect('/music/playlist/'+playlist_id)
    albums = Album.objects.filter(user = request.user)
    playlist = Playlist.objects.get(id = playlist_id)
    context = {
        'albums':albums,
        'playlist':playlist
    }
    return render(request,'music/addalbumstoplaylist.html',context)

'''
    function rename_playlist()
            takes playlist id 
            check if the user is owner
            sends or receives form
'''
def rename_playlist(request,playlist_id):
    currentPlaylist = Playlist.objects.get(id = playlist_id)
    form = RenamePlaylistForm(request.POST or None)
    if currentPlaylist.user==request.user:
        if request.method=="POST"  and form.is_valid() : 
            currentPlaylist.playlist_title = form.cleaned_data['new_playlist_title']
            currentPlaylist.save()
            return redirect('/music/playlist/'+playlist_id) 
        context = {'form':form,'old_name':currentPlaylist.playlist_title}
        return render(request,'music/rename_playlist.html',context)

'''
    function users()
        gets the user objects
        returns them
'''
def users(request):
    users = User.objects.all()
    return render(request,'music/users.html',{'users':users})

'''
    function view_user()
        if user and requested user are same then goes to home page
        get albums
        get songs
        sends data to view
'''
def view_user(request,user_id):
    if int(user_id) == request.user.id:
        return HttpResponseRedirect('/')
    albums = Album.objects.filter(user = user_id)
    searchedUser = User.objects.get(id=user_id)
    allsongs = Song.objects.filter(user = user_id )
    l = []
    for a in allsongs:
                l.append(a.audio_file.url)
    context = {'albums':albums,'l':l,'searched':True,'searchedUser':searchedUser}
    return render(request,'music/index.html',context)
