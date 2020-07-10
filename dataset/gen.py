import sys
from pathlib import Path
import mutagen
import requests
import os
from qtpy import QtWidgets, QtGui
import json

class ResultWidget(QtWidgets.QWidget):
    def __init__(self, item):
        super().__init__()
        self._item_data = {}

        self.layout = QtWidgets.QHBoxLayout()
        self.thumbnail = QtWidgets.QLabel()
        self.title = QtWidgets.QLabel()
        self.layout.addWidget(self.thumbnail, 0)
        self.layout.addWidget(self.title, 1)
        self.setLayout(self.layout)

    def _load_item(self, item):
        item_id = item.get("id")
        item_snippet = item.get("snippet")

        # set id
        if item_id.get("kind") != "youtube#video":
            raise ValueError
        self._item_data["id"] = item_id.get("videoId")

        # load title
        item_title = item_snippet.get("title")
        self._item_data["title"] = item_title
        self.title.setText(item_title)

        # load image
        thumbnail_url = item_snippet.get("thumbnails", {}).get("default", {}).get("url", None)
        if thumbnail_url is not None:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            self.thumbnail.setPixmap(pixmap)

class ResultsSelector(QtWidgets.QMainWindow):
    def __init__(self, items):
        super().__init__()
        self.setWindowTitle("Select results...")
        self.setFixedSize(300, 700)

        self.list_widget = QtWidgets.QListWidget(self)
        for item in items:
            try:
                result_widget = ResultWidget(item)

                list_item = QtWidgets.QListWidgetItem(self.list_widget)
                list_item.setSizeHint(result_widget.sizeHint())

                self.list_widget.addItem(list_item)
                self.list_widget.setItemWidget(list_item, result_widget)
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
