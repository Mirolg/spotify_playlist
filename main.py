from dotenv import load_dotenv
from os import getenv
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()


def download_titles(year: int) -> list:
    titles_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.select(".song-name > a")
    for song in songs:
        titles_list.append(song.text)
    return titles_list


def find_uri(downloaded_titles: list) -> list:
    songs_uri_list = []
    for title in downloaded_titles:
        result = sp.search(q=title)
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri_list.append(uri)
    return songs_uri_list


selected_years = int(input("Which years are you interested in? There are 60,70,80,90 to choose from: "))
url = f'https://www.stohitow.pl/przeboje-lat-{selected_years}'
if selected_years not in [60, 70, 80, 90]:
    print("Date entered incorrectly.")
else:
    titles = download_titles(selected_years)
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
    uri_song = find_uri(titles)
    user = sp.current_user()['id']
    create_playlist = sp.user_playlist_create(user=user, name=f"{selected_years}'s Hits", public=False)

    sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_song)

    print('Done, check your spotify account..')