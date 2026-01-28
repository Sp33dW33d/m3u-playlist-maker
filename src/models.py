from dataclasses import dataclass
from pathlib import Path

@dataclass
class AudioFile:
    path: Path 
    name: str
    duration: float
    artist: str = None
    normalized_name: str = None
    normalized_artist: str = None

    def pprint(self):
        print(f"path: {self.path}")
        print(f"name: {self.name}")
        print(f"duration: {self.duration}")
        print(f"artist: {self.artist}")
        print(f"normalized_name: {self.normalized_name}")
        print(f"normalized_artist: {self.normalized_artist}")

@dataclass
class Track:
    name: str
    duration: float
    artist: str
    normalized_name: str = None
    normalized_artist: str = None

    def pprint(self):
        print(f"name: {self.name}")
        print(f"duration: {self.duration}")
        print(f"artist: {self.artist}")
        print(f"normalized_name: {self.normalized_name}")
        print(f"normalized_artist: {self.normalized_artist}")
