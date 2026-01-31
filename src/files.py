import mutagen
import re
import pickle
from pathlib import Path
from src.models import AudioFile, Track

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)

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

def get_new_file_name(track: Track, count_iter: GeneratorExit) -> str:
    return f"{next(count_iter):03d} - {track.artist} - {track.name}.mp3"

def rename_file(old_audio_file: Path, new_audio_file: Path) -> None:
    try:
        old_audio_file.rename(new_audio_file)
    except OSError as e:
        print(e)

if __name__ == "__main__":
    ...