import pickle
from os import rename
import requests as req
import json
import re
import keys

# change this to f"{count} - {}"
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