from dotenv import load_dotenv
import os

from src import api 
from src import files
from src import matching

def get_api_keys() -> None:
    global CLIENT_ID, CLIENT_SECRET
    load_dotenv()
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET") 

def init() -> None:
    global PLAYLIST_LINK
    link = str(input("Enter the playlist link:\t")) 

if __name__ == "__main__":
    get_api_keys()

    link = "https://open.spotify.com/playlist/6vAVp8M1el9CLRe251q9Mg"
    PLAYLIST_ID = api.get_playlist_id(link)
    ACCESS_TOKEN = api.get_token(CLIENT_ID, CLIENT_SECRET)
    location = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\input"

    # tracks is the list[dict] of tracks retrieved from spotify
    tracks = api.get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
    tracks = matching.normalize_tracks(tracks)

    # audio_files is the list[str] of local audio_files stored at {location}
    audio_files = get_audio_files(location)
    audio_files = normalize_audio_files(audio_files)

# ---

    
