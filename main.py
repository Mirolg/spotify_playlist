import json

from dotenv import load_dotenv
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functions import download_titles, find_uri
from json import dump, load
load_dotenv()

action_choice = input('''
Do you want to create a playlist from a file or the best songs of the decade?
Press 1 or 2:
1 - from file.
2 - best song of the decade.
Choose: 
''')
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
if action_choice == '1':
    playlist_file_name = input('Podaj nazwe pliku: ')
    with open(f"{playlist_file_name}", 'r', encoding='utf8') as file:
        titles_json = json.load(file)
        titles_list = titles_json.get('titles')
    uri_song = find_uri(downloaded_titles=titles_list, spotipy=sp)
    create_playlist = sp.user_playlist_create(
        user=sp.current_user()['id'],
        name=f"{playlist_file_name.replace('.json','')}",
        public=False)
    print('Done, check your spotify account..')
    sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_song)

elif action_choice == '2':
    selected_years = int(input("Which years are you interested in? There are 60,70,80,90 to choose from: "))
    url = f'https://www.stohitow.pl/przeboje-lat-{selected_years}'
    if selected_years not in [60, 70, 80, 90]:
        print("Date entered incorrectly.")
    else:
        titles = download_titles(url_address=url)
        uri_song = find_uri(downloaded_titles=titles, spotipy=sp)
        create_playlist = sp.user_playlist_create(
            user=sp.current_user()['id'],
            name=f"{selected_years}'s Hits",
            public=False)

        sp.playlist_add_items(playlist_id=create_playlist['id'], items=uri_song)
        with open(f"{selected_years}'s Hits.json", 'w', encoding='utf8') as file:
            playlist = {
                'titles': titles
            }
            dump(playlist, file)
        print('Done, check your spotify account..')
else:
    print("The selected option is invalid.")
