import sys
from pathlib import Path
import mutagen
import requests
import os
from qtpy import QtWidgets, QtGui
import json

class ResultWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.thumbnail = QtWidgets.QLabel()
        self.layout.addWidget(self.thumbnail, 0)
        self.layout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.layout)

    def _set_thumbnail(self, image_path):
        self.thumbnail.setPixmap(QtGui.QPixmap(image_path))

class ResultsSelector(QtWidgets.QMainWindow):
    def __init__(self, items):
        super().__init__()
        self.setWindowTitle("Select results...")
        self.setFixedSize(300, 700)

        self.list_widget = QtWidgets.QListWidget(self)
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

# app = QtWidgets.QApplication(sys.argv)
# window = ResultsSelector()
# window.show()
# app.exec()
