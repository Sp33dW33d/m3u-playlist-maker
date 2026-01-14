import pickle
import requests as req
import json
import keys
import re

# def error_catcher(base_fn):
#     def enhanced_fn(*args, **kwargs):
#         response = base_fn(*args, **kwargs)
#         if response.status_code == 200:
#             return response
#         else:
#             return f"Error:, {response.status_code}, {response.text}"
#     return enhanced_fn

def get_token(client_id, client_secret):
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
    
def get_tracklist(playlist_id, access_token):
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset=0", headers = {"Authorization": f"Bearer {access_token}"})

    tracklist = []
    while True:
        for item in response.json()["items"]:
            tracklist.append(item["track"]["name"])
        next = response.json()["next"]
        if next == None:
            return tracklist
        else:
            response = req.get(url = next, headers = {"Authorization": f"Bearer {access_token}"})
            continue

def get_playlist_name(playlist_id, access_token):
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}", headers = {"Authorization": f"Bearer {access_token}"})

    return response.json()["name"]

def generate_playlist_file(playlist_name, tracklist):
    location = rf"Music/Playlists/{playlist_name}"    
    playlist_file = rf"D:\Coding_Stuff\Codes\Python\playlist-maker\data\{playlist_name}.m3u"
    # playlist_file = rf"D:\Coding_Stuff\Codes\Python\playlist-maker\data\uj_chill.m3u"

    with open(playlist_file, mode = "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for track in tracklist:
            f.write(f"{location} - {track}.mp3\n")
    
    return 1

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

if __name__ == "__main__":
    PLAYLIST_ID = "28tL7RsJGjCElo3cC8dty8"
    ACCESS_TOKEN = get_token(keys.CLIENT_ID, keys.CLIENT_SECRET)

    tracks = get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
    playlist_name = sanitize_filename(get_playlist_name(PLAYLIST_ID, ACCESS_TOKEN))
    if generate_playlist_file(playlist_name, tracks):
        print("Playlist file generated successfully")
