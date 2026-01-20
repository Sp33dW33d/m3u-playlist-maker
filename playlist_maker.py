import pickle
from os import rename
import requests as req
import json
import re
import keys

def get_token(client_id, client_secret) -> str:
    "returhs an access token"

    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    DATA = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
    }
    response = req.post(url = SPOTIFY_TOKEN_URL, headers = HEADERS, data = DATA)
    
    response.raise_for_status()
    return response.json()["access_token"]
    
def get_tracklist(playlist_id, access_token) -> list[tuple]:
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset=0", headers = {"Authorization": f"Bearer {access_token}"})

    tracklist = []
    while True:
        for item in response.json()["items"]:
            tracklist.append((item["track"]["artists"][0]["name"], item["track"]["name"]))
        next = response.json()["next"]
        if next == None:
            return tracklist
        else:
            response = req.get(url = next, headers = {"Authorization": f"Bearer {access_token}"})
            continue

def get_playlistid(playlistlink) -> str:
    return playlistlink.split("/")[-1]

def get_playlist_name(playlist_id, access_token) -> str:
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}", headers = {"Authorization": f"Bearer {access_token}"})
    return response.json()["name"]

def generate_trackline(location, track) -> str:
    return f"{location}/{track[0]} - {track[1]}.mp3\n"

def generate_playlist_file(playlist_name, tracklist):
    location = rf"Music/Playlists/{playlist_name}"
    playlist_file = rf"D:\Coding_Stuff\Codes\Python\playlist-maker\data\{playlist_name}.m3u"

    with open(playlist_file, mode = "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for track in tracklist:
            f.write(generate_trackline(location, track))
    
    return 1

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

# ---

if __name__ == "__main__":
    link = "https://open.spotify.com/playlist/28tL7RsJGjCElo3cC8dty8"
    PLAYLIST_ID = get_playlistid(link)
    ACCESS_TOKEN = get_token(keys.CLIENT_ID, keys.CLIENT_SECRET)

    tracks = get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
    playlist_name = sanitize_filename(get_playlist_name(PLAYLIST_ID, ACCESS_TOKEN))
    if generate_playlist_file(playlist_name, tracks):
        print("Playlist file generated successfully")
    