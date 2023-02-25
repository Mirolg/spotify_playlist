import requests
from bs4 import BeautifulSoup


def download_titles(year: int, url_address: str) -> list:
    """
    The function retrieves the titles of the top 100 songs from the given decade.
    :param year: The decade from which the playlist is to be created.
    :param url_address: URL of the page from which the song titles are downloaded.
    :return: List of song titles.
    """
    titles_list = []
    response = requests.get(url_address)
    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.select(".song-name > a")
    for song in songs:
        titles_list.append(song.text)
    return titles_list


def find_uri(downloaded_titles: list, spotipy) -> list:
    """
    The function for the given list of titles searches for a unique resource indicator code
    that allows you to search for songs on spotify.
    :param downloaded_titles: List of titles for which unique codes are to be found.
    :param spotipy: Client Authorization Code Flow Spotipy
    :return: List of unique codes corresponding to song titles on spotify.
    """
    songs_uri_list = []
    for title in downloaded_titles:
        result = spotipy.search(q=title)
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri_list.append(uri)
    return songs_uri_list
