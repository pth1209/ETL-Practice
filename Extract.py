import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def get_recently_played_track():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    scope = "user-read-recently-played"

    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )

    token_info = sp_oauth.get_access_token(as_dict=True)
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    sp = spotipy.Spotify(auth=token_info['access_token'])

    data = sp.current_user_recently_played(limit=50)

    song_names, artists, played_at, timestamp = [], [], [], []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artists.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamp.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist": artists,
        "played_at": played_at,
        "timestamp": timestamp
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist", "played_at", "timestamp"])
    return song_df
