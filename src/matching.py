import rapidfuzz
import os
import re
from src.models import AudioFile, Track
from pickle import load

def normalize_string(string: str) -> str:
    NOISE_WORDS = {
        "official", "audio", "video", "lyrics", "lyric",
        "remastered", "remaster", "hq", "hd", "320kbps",
        "explicit", "clean"}

    string = string.lower()
    string = re.sub(r'\.[a-z0-9]{2,4}$', '', string)   # remove extension
    string = re.sub(r'[\[\(].*?[\]\)]', '', string)    # remove brackets
    string = re.sub(r'[_\-]+', ' ', string)            # unify separators
    
    words = []
    for word in string.split():
        cleaned = ''.join(ch for ch in word if ch.isalnum())
        if cleaned and cleaned not in NOISE_WORDS and not cleaned.isdigit():
            words.append(cleaned)

    return " ".join(words)

def normalize_audio_files(audio_files: list[AudioFile]) -> list[AudioFile]:
    """adds normalized_name and normalized_artist to the AudioFile objs"""

    normalized_audio_files = []
    for audio_file in audio_files:
        audio_file.normalized_name = normalize_string(audio_file.name)
        audio_file.normalized_artist = normalize_string(audio_file.artist)
        normalized_audio_files.append(audio_file)
    
    return normalized_audio_files

def normalize_tracks(tracks: list[Track]) -> list[Track]:
    """adds normalized_name and normalized_artist to the Track objs"""
    
    normalized_tracks = []
    for track in tracks:
        track.normalized_name = normalize_string(track.name)
        track.normalized_artist = normalize_string(track.artist)
        normalized_tracks.append(track)    
    
    return normalized_tracks    

def score_title_similarity(track_title: str, file_title: str) -> float:
    return rapidfuzz.fuzz.partial_ratio(track_title, file_title)

# since im only using normalization for now, artist_similarity assumes the artist's name is also present in the file_name
# ideal behaviour should be to default to tag based similarity calculation, but resorting to file_name based search if tag doesnt exist
# will add tags based searching later
def score_artist_similarity(track_artist: str, file_artist: str) -> float:
    return rapidfuzz.fuzz.partial_ratio(track_artist, file_artist)

def score_duration_similarity(track_duration: float, file_duration: float) -> float:
    MAX_TOLERANCE = 10
    return 1.0 - abs(track_duration - file_duration)/MAX_TOLERANCE

def compute_match_score(track_obj: Track, file_obj: AudioFile,
                        weights={"title": 0.5,
                                "artist": 0.3,
                                "duration": 0.2}) -> float:

    title_similarity = score_title_similarity(track_obj.normalized_name, file_obj.normalized_name)
    artist_similarity = score_artist_similarity(track_obj.normalized_artist, file_obj.normalized_artist)
    duration_similarity = score_duration_similarity(track_obj.duration, file_obj.duration)
    
    final_score = ((weights["title"] * title_similarity) + 
                  (weights["artist"] * artist_similarity) + 
                  (weights["duration"] * duration_similarity)) 

    return final_score

def find_best_match(track_obj: Track, audio_files: list[AudioFile], SCORE_CUTOFF = 0) -> tuple:
    best_match = None
    best_score = 0

    for file_obj in audio_files:
        score = compute_match_score(track_obj, file_obj)
        if score > best_score and score > SCORE_CUTOFF:
            best_match = file_obj
            best_score = score

    return (best_match, best_score)

    # after i do find the best match. i need to get the original audio_file_name so i can rename it
    # but how am i supposed to get the original audio_file_name from the normalized_file_name...?
    # ugh i guess i need to make a Track class, and a File class


    # what the fuck??? ternary operator AND list comprehension? 
    # return [track if compute_match_score(track, audio_file) >= SCORE_CUTOFF][-1] if [track if compute_match_score(track, audio_file) >= SCORE_CUTOFF] else None

if __name__ == "__main__":
    file = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\audio_files.femboy"
    
    with open(file, "rb") as f:
        audio_files = load(f)

    normalized_audio_files = normalize_audio_files(audio_files)
    
    for audio_file in normalized_audio_files:
        audio_file.pprint()
        print("----", end="\n")