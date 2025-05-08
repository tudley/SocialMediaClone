import os
from SpotifyAPI.request_testing import post, get
import base64
import json

from dotenv import load_dotenv

load_dotenv()

# here we fetch out client credentials from a seperate, secure .env file
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token():
    """Here we are generating and returning our token to access the spotify web API"""

    # Spotify required a base64 encoded string of "client_id:client_secret"
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


def search_for_artist(token, artist):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"q={artist}&type=artist&limit=1"
    query_url = url + '?' + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print('no artists found...')
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UK"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


token = get_token()
#print(token)
result = search_for_artist(token, 'outkast')
#print(result)
artist_id = result['id']
print(artist_id)
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}.{song['name']}")


