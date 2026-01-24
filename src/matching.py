"""
notes

preprocessing is required, damn
need to strip, probably remove the artist name(?)
ehh but should i do string based removal? what if i use a different source for the music files. 
or just that the music file names have a different formatting

i guess i could do searches based on the mp3 file's metadata tags
but some sources might not provide tags sooo... idk
maybe i should add 2 different modes
filename based search, and tag based search
and maybe for filename based search, i should add different modes to allow for different mp3 file naming formats. eh.
would be a lot of hard coding maybe
"""
# func for getting the song_files
# func for getting the song_name

# func for getting best name match
# func for getting artist match
# func for getting duration match
# func for calculating overall similarity for one file
# func for getting best overall match

# func for renaming a specific file
# func for running the loop

import rapidfuzz
import os
import re
# probably need to use mutagen to get file duration

def normalize_name(name: str) -> str:
    NOISE_WORDS = {
        "official", "audio", "video", "lyrics", "lyric",
        "remastered", "remaster", "hq", "hd", "320kbps",
        "explicit", "clean"}

    name = name.lower()
    name = re.sub(r'\.[a-z0-9]{2,4}$', '', name)   # remove extension
    name = re.sub(r'[\[\(].*?[\]\)]', '', name)    # remove brackets
    name = re.sub(r'[_\-]+', ' ', name)            # unify separators
    
    words = []
    for word in name.split():
        cleaned = ''.join(ch for ch in word if ch.isalnum())
        if cleaned and cleaned not in NOISE_WORDS and not cleaned.isdigit():
            words.append(cleaned)

    return " ".join(words)

def normalize_audio_files(audio_files: list) -> list[str]:
    return [normalize_name(file) for file in audio_files]

def normalize_tracks(tracks: list[dict]) -> list[dict]:
    for track in tracks:
        track["artist"] = normalize_name(track["artist"])
        track["name"] = normalize_name(track["name"])
    return tracks    

def score_title_similarity(song_name: str, file_name: str) -> float:
    return rapidfuzz.partial_ratio(song_name, file_name)

def score_artist_similarity(artist_name: str, file_name: str) -> float:
    return rapidfuzz.partial_ratio(artist_name, file_name)

def score_duration_similarity(song_duration: int, file_duration: int) -> float:
    MAX_TOLERANCE = 10
    return 1.0 - abs(song_duration - file_duration)/MAX_TOLERANCE

def compute_match_score(track, audio_file, 
                        weights={"title": 0.5,
                                "artist": 0.3,
                                "duration": 0.2}):

    title_similarity = score_title_similarity(track["name"], audio_file)
    artist_similarity = score_title_similarity(track["artist"], audio_file)
    # need to do something about the duration
    duration_similarity = score_title_similarity(track["duration"], audio_file.info.length)
    
    final_score = ((weights["title"] * title_similarity) + 
                  (weights["artist"] * artist_similarity) + 
                  (weights["duration"] * duration_similarity)) 

    return final_score

def find_best_match(tracks: list[dict], audio_file: str):
    # SCORE_CUTOFF = 0.80
    # candidates = []

    # for track in tracks:
    #     if compute_match_score(track, audio_files) >= SCORE_CUTOFF:
    #         candidates.append[track]
    # return candidates[-1] if candidates else None

    # what the fuck??? ternary operator AND list comprehension? 
    return [track if compute_match_score(track, audio_file) >= SCORE_CUTOFF][-1] if [track if compute_match_score(track, audio_file) >= SCORE_CUTOFF] else None

if __name__ == "__main__":
    # test_song  = {"artist": "Snail's House",
    #             "name": "Cosmo Funk",
    #             "duration": 3000}
        # print(test_song)

    song_name = "City Girl - HEARTBREAKER CLUB.mp3"
    audio_files = ['Cement City - Here Comes a Thought.mp3', 'Chevy - UWU (Band Version).mp3', 'Chevy - UWU.mp3', 'City Girl - HEARTBREAKER CLUB.mp3', 'Claire Rosinkranz - Backyard Boy.mp3', "Hyper_Potions_K_K_Cruisin'_From__Animal_Crossing_.mp3", 'Lilypichu - dreamy night.mp3', 'Makzo - Blossom.mp3', 'Mindy Gledhill - I Do Adore.mp3', 'mxmtoon - fever dream (Shawn Wasabi remix).mp3', 'potsu - just friends.mp3', 'Wave Racer - Higher.mp3', '달콤한꿈 - 꽃날 (황진이 OST).mp3']
    
    audio_files = normalize_audiofiles(audio_files)
    print(audio_files)