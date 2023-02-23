import requests
from bs4 import BeautifulSoup

url = 'https://www.stohitow.pl/przeboje-lat-70'
song_list = []
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select(".song-name > a")
for song in songs:
    song_list.append(song.text)


print(song_list)