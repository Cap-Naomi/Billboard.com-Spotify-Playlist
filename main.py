import requests, pprint
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
# used Spotify API, Spotipy library, OAuth Authentication

#### Scrapes Billboard's top 100 songs and stores song titles in a list
URL = "https://www.billboard.com/charts/year-end/2025/hot-100-songs/"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
response = requests.get(URL, headers=headers)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
songs = soup.select("li #title-of-a-story")
all_artists = soup.select("li span a")

song_titles = [title.text.strip() for title in songs]
# artists = [artist.get_text() for artist in all_artists]

#### Links your Spotify account to spotipy to access/edit your library
client_id = "your client id"
client_secret = "your client secret"
redirect_uri = "http://127.0.0.1:9090"

client_manager = SpotifyClientCredentials(client_id, client_secret)
auth_manager = SpotifyOAuth(
    client_id= client_id,
    client_secret= client_secret,
    redirect_uri= redirect_uri,
    scope= "playlist-modify-private"
)

spotify = spotipy.Spotify(client_credentials_manager= client_manager, auth_manager=auth_manager)
user_id = spotify.current_user()["id"]

#### Searches track name in Spotify to return track uri
track_uris = []
for song in song_titles:
    result = spotify.search(q=f"track:{song} year:2025", type="track", limit=1)
    try:
        song_uri = result["tracks"]["items"][0]["uri"]
        track_uris.append(song_uri)
    except IndexError:
        print(f"Error: Couldn't find song: '{song}'.")

#### creates new playlist and adds tracks from track_uris
playlist = spotify.user_playlist_create(
    user= user_id,
    name= "2025 Top 100 Songs - Billboard",
    public=False,
    description= "Playlist created from songs listed on Billboard.com"
)
print(playlist)

spotify.playlist_add_items(
    playlist_id= playlist["id"],
    items=track_uris
)

print("\nCongrats, your new playlist is created!\n")

