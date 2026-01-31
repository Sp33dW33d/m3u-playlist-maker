import requests as req
import json
from src.models import Track

def get_token(client_id, client_secret) -> str:
    "returhs an access token"

    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    DATA = {'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret}
    response = req.post(url = SPOTIFY_TOKEN_URL, headers = HEADERS, data = DATA)
    
    response.raise_for_status()
    return response.json()["access_token"]

def get_playlist_id(playlist_link) -> str:
    return playlist_link.split("/")[-1]

def get_playlist_name(playlist_id, access_token) -> str:
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}", headers = {"Authorization": f"Bearer {access_token}"})
    return response.json()["name"]

def get_tracklist(playlist_id, access_token) -> list[Track]:
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset=0", headers = {"Authorization": f"Bearer {access_token}"})

    tracklist = []
    while True:
        for item in response.json()["items"]:
            tracklist.append(
                Track(name = item["track"]["name"],
                      duration = item["track"]["duration_ms"],
                      artist = item["track"]["artists"][0]["name"])
            )
        next = response.json()["next"]
        if next != None:
            response = req.get(url = next, headers = {"Authorization": f"Bearer {access_token}"})
            continue
        else:
            return tracklist