import sys
from pathlib import Path
import mutagen
import requests
import os

def youtube_api(endpoint, params):
    payload = {
        "part": "snippet",
        "maxResults": 50,
    }
    try:
        payload["key"] = os.environ["YOUTUBE_API_KEY"]
    except KeyError:
        print("Warning: no youtube access token provided")
    payload.update(params)

    headers = {
        "accept": "application/json"
    }
    try:
        headers["authorization"] = "Bearer " + os.environ["YOUTUBE_ACCESS_TOKEN"]
    except KeyError:
        print("Warning: no youtube access token provided")

    return requests.get(endpoint, params=payload, headers=headers).json()

def youtube_search(query, **kwargs):
    params = {
        "q": query
    }
    params.update(kwargs)
    a = youtube_api("https://www.googleapis.com/youtube/v3/search", params)

try:
    songs_path = sys.argv[1]

    for path in Path(songs_path).rglob('*.mp3'):
        song_file = mutagen.File(path, easy=True)
        try:
            title = song_file['title']
            artist = song_file['artist']
        except KeyError:
            print("Warning: skipped song file due to improper metadata: {}".format(path.relative_to(songs_path)))

except IndexError:
    print("Please provide a songs path")
