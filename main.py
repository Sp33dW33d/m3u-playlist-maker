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
        audio_files = files.get_audio_files(DATA_DIR)
        pickle.dump(audio_files, f)
        
def read_files(tracks_path, audio_files_path):
    with open(tracks_path, "rb") as f:
        tracks = pickle.load(f)

    with open(audio_files_path, "rb") as f:
        audio_files = pickle.load(f)
    
    return tracks, audio_files

def print_match_scores(track_obj: Track, normalized_audio_files: list[AudioFile]):
    matching_scores = []    
    for file_obj in normalized_audio_files:
        match_score = matching.compute_match_score(track_obj,file_obj)
        matching_scores.append(
            (file_obj, match_score)
        )

    for (file_obj, match_score) in matching_scores:
        print(f"{track_obj.name}\t-\t{file_obj.name:^50}\t-\t{match_score:>20}")

def print_best_match(track_obj: Track, best_match: AudioFile, best_score: float):
    if best_match is not None:
        print()
        print(f"{track_obj.name}'s best match was\n{best_match.path}\nwith a score of {best_score}")
        print()
    else:
        print("No match found!")

def print_names(old_name, new_name):
    print(f"{'Original name:':<30} {' ':^20} {old_name:>30}")
    print(f"{'New name:':<30} {' ':^20} {new_name:>30}")

def generate_log_file(LOG_DIR, log_lines: list):
    with open(LOG_DIR / "log.txt", "w") as f:
        f.writelines(log_lines)

def mainloop():
    get_api_keys()

    PLAYLIST_ID = api.get_playlist_id(link)
    ACCESS_TOKEN = api.get_token(CLIENT_ID, CLIENT_SECRET)
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data" / "input"
    LOG_DIR = BASE_DIR / "data" / "logs"

    # ---
    # fetches the tracks and audio_files lists

    if read_from_files:
        tracks_path = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\tracks.tomboy"
        audio_files_path = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\audio_files.femboy"
    
        tracks, audio_files = read_files(tracks_path, audio_files_path)
    else:
        tracks = api.get_tracklist(PLAYLIST_ID, ACCESS_TOKEN)
        audio_files = files.get_audio_files(DATA_DIR)

    # ---
    # normalizes the lists

    tracks = matching.normalize_tracks(tracks)
    audio_files = matching.normalize_audio_files(audio_files)

    # ---

    # print_match_scores(track_obj, audio_files)
    # print_best_match(track_obj, audio_files)

    # ---

    count_iter = files.counter()
    log_lines = []

    for track_obj in tracks:
        best_match, best_score = matching.find_best_match(track_obj, audio_files)
        if best_score < SCORE_CUTOFF:
            print(f"No match found for \"{track_obj.name}\"!")
            print("Skipping...")
            
            log_lines.append(
                f"Count: {next(count_iter)}\nName: {track_obj.name}\nBest match: {best_match.path}\n"
            )        
            
        else:
            print_best_match(track_obj, best_match, best_score)
            new_name = files.get_new_file_name(track_obj, count_iter)
            new_name = files.sanitize_filename(new_name)

        print_names(track_obj.name, new_name)
        print()

        new_file_path = DATA_DIR / new_name
        files.rename_file(best_match.path, new_file_path)
        print(f"{best_match.path}\nhas been renamed to\n{new_file_path}")
        print("\n--------------------")
    
    generate_log_file(LOG_DIR, log_lines)
    # ---

if __name__ == "__main__":
    # FLAGS
    read_from_files = 0
    SCORE_CUTOFF = 50
    link = "https://open.spotify.com/playlist/28tL7RsJGjCElo3cC8dty8"

    mainloop()
    
    # ---