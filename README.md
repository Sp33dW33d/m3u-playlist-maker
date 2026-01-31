# Description

Automatically aligns locally stored audio files with a Spotify playlist using fuzzy matching, metadata heuristics, and confidence-based decision making.

In other words, renames files in the data/input folder based on the order of the spotify playlist provided.

# How to run
python main.py

# Documentation
main.py imports files.py, api.py and matching.py

files.py - responsible for file handling like getting list of audio files, renaming files etc
api.py - responsible for handling api calls to spotify, returning list of items from a playlist etc
matching.py - responsible for confidence based matching between the local audio files and the songs from spotify
models.py - custom Track and AudioFIle classes 