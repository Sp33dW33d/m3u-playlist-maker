from dotenv import load_dotenv
from os import getenv
from pathlib import Path
import pickle

from src import api 
from src import files
from src import matching
from src.models import AudioFile, Track

def get_api_keys() -> None:
    global CLIENT_ID, CLIENT_SECRET
    load_dotenv()
    # CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET") 

def write_files(tracks_path, audio_files_path): 
    global PLAYLIST_ID, ACCESS_TOKEN

    with open(tracks_path, "wb") as f:
        tracks = api.get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
        pickle.dump(tracks, f)

    with open(audio_files_path, "wb") as f:
        audio_files = files.get_audio_files(Path(__file__).resolve().parent / "data" / "input")
        pickle.dump(audio_files, f)
        
def read_files(tracks_path, audio_files_path):
    with open(tracks_path, "rb") as f:
        tracks = pickle.load(f)

    with open(audio_files_path, "rb") as f:
        audio_files = pickle.load(f)
    
    return tracks, audio_files
    

if __name__ == "__main__":
    get_api_keys()

    link = "https://open.spotify.com/playlist/6vAVp8M1el9CLRe251q9Mg"
    PLAYLIST_ID = api.get_playlist_id(link)
    ACCESS_TOKEN = api.get_token(CLIENT_ID, CLIENT_SECRET)
    location = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\input"

    # # tracks is the list[Track] of tracks retrieved from spotify
    # tracks = api.get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
    # tracks = matching.normalize_tracks(tracks)

    # # audio_files is the list[AudioFile] of local audio_files stored at {location}
    # audio_files = get_audio_files(location)
    # audio_files = normalize_audio_files(audio_files)

    # ---
    
    tracks_path = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\tracks.tomboy"
    audio_files_path = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\audio_files.femboy"
    
    # write_files(tracks_path, audio_files_path)
    tracks, audio_files = read_files(tracks_path, audio_files_path)
    
    normalized_tracks = matching.normalize_tracks(tracks)
    normalized_audio_files = matching.normalize_audio_files(audio_files)

    track_obj = normalized_tracks[2]
    
    matching_scores = []
    for file_obj in normalized_audio_files:
        matching_scores.append(
            (file_obj, matching.compute_match_score(track_obj,file_obj))
        )

    for (file_obj, match_score) in matching_scores:
        print(f"{track_obj.name}\t-\t{file_obj.name:^50}\t-\t{match_score:>20}")

    best_match, best_score = matching.find_best_match(track_obj, normalized_audio_files)
    if best_match is not None:
        print()
        print(f"{track_obj.name}'s best match was\n{best_match.path}\nwith a score of {best_score}")
        print()
    else:
        print("No match found!")
    
    # ---

