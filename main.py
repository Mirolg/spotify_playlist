from dotenv import load_dotenv
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functions import download_titles, find_uri
load_dotenv()


selected_years = int(input("Which years are you interested in? There are 60,70,80,90 to choose from: "))
url = f'https://www.stohitow.pl/przeboje-lat-{selected_years}'
if selected_years not in [60, 70, 80, 90]:
    print("Date entered incorrectly.")
else:
    titles = download_titles(year=selected_years, url_address=url)
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
    uri_song = find_uri(downloaded_titles=titles,spotipy=sp)
    create_playlist = sp.user_playlist_create(
        user=sp.current_user()['id'],
        name=f"{selected_years}'s Hits",
        public=False)

    sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_song)

    print('Done, check your spotify account..')
