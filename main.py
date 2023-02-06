import re
import requests
import pprint
import spotipy
from bs4 import BeautifulSoup

CLIENT_ID = ""
SECRET = ""
scopes = [
    "user-read-currently-playing",
    "user-read-recently-played",
    "user-read-playback-state",
    "user-top-read",
    "user-modify-playback-state",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public"
]

client_credentials = spotipy.SpotifyClientCredentials(CLIENT_ID, SECRET)
something = spotipy.SpotifyOAuth(client_id=CLIENT_ID, client_secret=SECRET, scope=scopes,
                                 redirect_uri="http://localhost:8888/callback", username="31fgqufdtf5an63wmpdyrlgkrrme")
spotify = spotipy.Spotify(oauth_manager=something)

# data = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

date = "2022-01-12"
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")

html = response.text

soup = BeautifulSoup(html, "html.parser")
songs_name = soup.find_all("h3", class_=[
    "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
    "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"])
artists = soup.find_all("span", class_=[
    "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet",
    "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only",
    "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"])

songs_titles = [re.sub('[^\S ]+', '', song.getText()) for song in songs_name]
artists_names = [re.sub('[^\S ]+', '', artist.getText()) for artist in artists]

print(songs_titles)
print(artists_names)
songs = []
for i, song in enumerate(songs_titles):
    try:
        song_id = spotify.search(q=f"track: {song} artist: {artists_names[i]}", type='track', market="PL", limit=1) \
            ['tracks']['items'][0]['uri']
        songs.append(song_id)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist_id = spotify.user_playlist_create("31fgqufdtf5an63wmpdyrlgkrrme",f"{date} 100 TOP HITS",public=False)
spotify.playlist_add_items(playlist_id['id'], songs, position=None)
