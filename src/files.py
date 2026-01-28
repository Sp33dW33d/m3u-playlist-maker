import mutagen
import re
import pickle
from pathlib import Path
from src.models import AudioFile

# def sanitize_filename(filename: str) -> str:
#     return re.sub(r'[\\/:*?"<>|]', '_', filename)

# add filename functionality... maybe?
def get_audio_files(data_dir: Path) -> list[AudioFile]:
    audio_files = []
    
    for file_path in data_dir.iterdir():
        file_obj = mutagen.File(file_path)
        audio_files.append(
            AudioFile(
                path = file_path, 
                name = str(file_obj["TIT2"]), 
                duration = float(file_obj["TLEN"].text[0]),
                artist = str(file_obj["TPE1"][0])
            )
        )
    return audio_files
    
def counter(start: int = 1) -> int:
    n = start
    while True:
        yield n
        n += 1

def get_new_file_name(track: dict) -> str:
    return f"{next(count):03d} - {track["artist"]} - {track["name"]}"

def rename_file(current_name, new_name) -> None:
    try:
        current_file = DATA_DIR / current_name
        new_file = DATA_DIR / new_file
        current_file.rename(new_file)

        print(f"\"{current_name}\" has been renamed to \"{new_name}\"")
    except Error as e:
        print(e)

if __name__ == "__main__":
    file = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\audio_files.femboy"
    
    with open(file, "wb") as f:
        audio_files = get_audio_files()
        pickle.dump(audio_files, f)

    # with open(file, "rb") as f:
    #     audio_files = pickle.load(f)
    #     for audio_file in audio_files:
    #         print(type(audio_file.artist))
    #         print(type(audio_file.name))
    #         print(type(audio_file.duration))
    #         print("-----")