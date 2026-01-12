import pickle
import requests as req
import json
import keys

# def error_catcher(base_fn):
#     def enhanced_fn(*args, **kwargs):
#         response = base_fn(*args, **kwargs)
#         if response.status_code == 200:
#             return response
#         else:
#             return f"Error:, {response.status_code}, {response.text}"
#     return enhanced_fn

# @error_catcher
def get_token(client_id, client_secret):
    "returhs an access token"

    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    DATA = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
    }
    response = req.post(url = SPOTIFY_TOKEN_URL, headers = HEADERS, data = DATA)
    
    response.raise_for_status()
    return response.json()["access_token"]
    
# @error_catcher
def get_tracklist(playlist_id, access_token, mode = 1): 
    "returns complete list of tracks"

    response = req.get(url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset=0", headers = {"Authorization": f"Bearer {access_token}"})
    
    response.raise_for_status()

    if mode == 1:
        tracks = []
        for item in response.json()["items"]: 
            tracks.append(item["track"]["name"])
        return tracks
    else:
        return response    



if __name__ == "__main__":
    # ACCESS_TOKEN = get_token(keys.CLIENT_ID, keys.CLIENT_SECRET)
    # ACCESS_HEADER = {
    #     "Authorization": f"Bearer {ACCESS_TOKEN}"
    # }

    file = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\playlist_info.bin"
    
    try:
        with open(file, mode= "rb") as f:
            tracklist = pickle.load(f)
    except FileNotFoundError:
        with open(file, mode="wb") as f:
            tracklist = get_tracklist("106NJsdPB7rXgX1i7CmpLn")
            pickle.dump(tracklist, f)

    print(tracklist)

    playlist_file = r"D:\Coding_Stuff\Codes\Python\playlist-maker\data\playlist.m3u"
    
    with open(playlist_file, mode = "w", encoding="utf-8") as f:
        f.write("#EXTM3U")
        for track in tracklist:
            f.write(f"{track}\n")
