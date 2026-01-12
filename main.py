import playlist_maker as pm
import keys
import pickle
import requests as req

def gget_tracklist(playlist_id, access_token):
    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset=0", headers = {"Authorization": f"Bearer {access_token}"})

    tracks = []
    while True:
        for item in response.json()["items"]:
            tracks.append(item["track"]["name"])
        next = response.json()["next"]
        if next == None:
            return tracks
        else:
            response = req.get(url = next, headers = {"Authorization": f"Bearer {access_token}"})
            continue


# ----------------

# ACCESS_TOKEN = pm.get_token(keys.CLIENT_ID, keys.CLIENT_SECRET)
# print(ACCESS_TOKEN)

ACCESS_TOKEN = "BQAVnwsUCZfMkNNb2wJ5KO88Qi0R451WJJ1Tlj_99HfGepQ2OqTSjXVhf4sBnp9hg1m1nMvl9sPdM3cyoPlfpiOAYnMbvuRoNx1eg95kr2GE_ZskQD4gnAe2QIYznRoFLSA8Bwri1AU"

# file = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\playlist_json.bin"

# try:
#     with open(file, mode= "rb") as f:
#         playlist_items_json = pickle.load(f)
# except FileNotFoundError:
#     with open(file, mode="wb") as f: 
#         playlist_items_json = pm.get_tracklist("28tL7RsJGjCElo3cC8dty8", ACCESS_TOKEN, mode = 2)
#         pickle.dump(playlist_items_json, f)

# print(playlist_items_json.json()["limit"])
# print(playlist_items_json.json()["offset"])
# print(playlist_items_json.json()["next"])
# print(playlist_items_json.json()["total"])

tracks = gget_tracklist("28tL7RsJGjCElo3cC8dty8", ACCESS_TOKEN)
print(tracks)
print(len(tracks))
