from dotenv import load_dotenv, find_dotenv
import requests
import base64
import json
import os

load_dotenv(find_dotenv())
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN").strip()
CLIENT_ID = os.environ.get("CLIENT_ID").strip()
CLIENT_SECRET = os.environ.get("CLIENT_SECRET").strip()
DISCOVER_WEEKLY_ID = os.environ.get("DISCOVER_WEEKLY_ID").strip()
SAVE_TO_ID = os.environ.get("SAVE_TO_ID").strip()

DISCOVER_WK_IDS = [
  os.environ.get("DISCOVER_WK_ID_0").strip(),
  os.environ.get("DISCOVER_WK_ID_1").strip(),
  os.environ.get("DISCOVER_WK_ID_2").strip(),
  os.environ.get("DISCOVER_WK_ID_3").strip()
]

DESTINATION_IDS = [
  os.environ.get("DESTINATION_ID_0").strip(),
  os.environ.get("DESTINATION_ID_1").strip(),
  os.environ.get("DESTINATION_ID_2").strip(),
  os.environ.get("DESTINATION_ID_3").strip()
]

OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
def refresh_access_token():
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
    }
    encoded_client = base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode('ascii'))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % encoded_client.decode('ascii')
    }
    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    return response.json()


def get_playlist(access_token, discover_wk_id):
    url = "https://api.spotify.com/v1/playlists/%s" % discover_wk_id
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.get(url, headers=headers)
    return response.json()

def add_to_playlist(access_token, tracklist, destination_id):
    url = "https://api.spotify.com/v1/playlists/%s/tracks" % destination_id
    payload = {
        "uris" : tracklist
    }
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()


def main():
    if REFRESH_TOKEN is None or CLIENT_ID is None or CLIENT_SECRET is None:
        print("Environment variables have not been loaded!")
        return

    access_token = refresh_access_token()['access_token']

    for i in range(len(DISCOVER_WK_IDS)):
        tracks =  get_playlist(access_token, DISCOVER_WK_IDS[i])['tracks']['items']
        tracklist = []
        for item in tracks:
            tracklist.append(item['track']['uri'])
        response = add_to_playlist(access_token, tracklist, DESTINATION_IDS[i])

        if "snapshot_id" in response:
            print("Successfully added all songs")
        else:
            print(response)

main()