import playlist_maker as pm
import keys
import pickle
import requests as req

# ----------------

# ACCESS_TOKEN = pm.get_token(keys.CLIENT_ID, keys.CLIENT_SECRET)
# print(ACCESS_TOKEN)

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
