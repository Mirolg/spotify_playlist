from dotenv import load_dotenv
from os import getenv
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

url = 'https://www.stohitow.pl/przeboje-lat-70'
song_list = []
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select(".song-name > a")
for song in songs:
    song_list.append(song.text)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        client_id=getenv('CLIENT_ID'),
        client_secret=getenv('CLIENT_SECRET'),
        redirect_uri="http://localhost:8888/callback",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user = sp.current_user()['id']
uri_song = []

for song in songs:
    results = sp.search(q=song)
    uri = results["tracks"]["items"][0]["uri"]
    uri_song.append(uri)

create_playlist = sp.user_playlist_create(user=user, name="70's Hits", public=False)

sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_song)

print('complete')