from dotenv import load_dotenv
import os

from src import api 
from src import playlist_maker as pm

def get_api_keys():
    global CLIENT_ID, CLIENT_SECRET
    load_dotenv()
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET") 

if __name__ == "__main__":
    get_api_keys()

    link = "https://open.spotify.com/playlist/28tL7RsJGjCElo3cC8dty8"
    PLAYLIST_ID = pm.get_playlistid(link)
    ACCESS_TOKEN = pm.get_token(CLIENT_ID, CLIENT_SECRET)

    tracks = pm.get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
    playlist_name = pm.sanitize_filename(get_playlist_name(PLAYLIST_ID, ACCESS_TOKEN))
    if generate_playlist_file(playlist_name, tracks):
        print("Playlist file generated successfully")
