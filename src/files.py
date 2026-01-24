from os import rename
import re

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def get_audio_files(location: str) -> list[str]:
    return os.listdir(location)

def counter(start = 1: int) -> int:
    n = start
    while True:
        yield n
        n += 1

def get_new_file_name(track: dict) -> str:
    return f"{next(count):03d} - {track["artist"]} - {track["name"]}"

def rename_file(current_name, new_name) -> None:
    try:
        rename(current_name, new_name)
        print(f"\"{current_name}\" has been renamed to \"{new_name}\"")
    except Error as e:
        print(e)
