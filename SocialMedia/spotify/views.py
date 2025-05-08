from django.shortcuts import render
from SpotifyAPI import get_token, search_for_artist, get_auth_header, get_songs_by_artist
import os

def home(request, artist):
    """This page """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    token = get_token()
    result = search_for_artist(token, artist)
    artist_id = result['id']
    songs = get_songs_by_artist(token, artist_id)
    



    return render(request, 'spotify/home.html')

