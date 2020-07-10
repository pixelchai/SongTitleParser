import sys
from pathlib import Path
import mutagen
import requests
import os
from qtpy import QtWidgets, QtGui, QtCore
import json
import html

class ResultsSelector(QtWidgets.QMainWindow):
    def __init__(self, items):
        super().__init__()
        self.setWindowTitle("Select results...")
        self.setFixedSize(510, 700)
        self.items = []

        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setIconSize(QtCore.QSize(256, 256))
        self.list_widget.setWordWrap(True)
        for item in items.get("items", []):
            try:
                list_item = None

                item_data = {}
                item_id = item.get("id")
                item_snippet = item.get("snippet")

                # set id
                if item_id.get("kind") != "youtube#video":
                    raise ValueError
                item_data["id"] = item_id.get("videoId")

                # load title
                item_title = html.unescape(item_snippet.get("title", ""))
                item_data["title"] = item_title

                # load image
                thumbnail_url = item_snippet.get("thumbnails", {}).get("default", {}).get("url", None)
                if thumbnail_url is not None:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(requests.get(thumbnail_url).content)
                    list_item = QtWidgets.QListWidgetItem(QtGui.QIcon(pixmap), item_title, self.list_widget)
                    self.list_widget.addItem(list_item)

                self.items.append(item_data)
            except ValueError:
                pass

        self.setCentralWidget(self.list_widget)

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
    return youtube_api("https://www.googleapis.com/youtube/v3/search", params)

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

# with open("out.json", "w") as f:
#     json.dump(youtube_search("akane sasu"), f)

with open("out.json", "r") as f:
    app = QtWidgets.QApplication(sys.argv)
    window = ResultsSelector(json.load(f))
    window.show()
    app.exec()
