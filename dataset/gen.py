import sys
from pathlib import Path
import mutagen
import requests
import os
from qtpy import QtWidgets, QtGui, QtCore
import json
import html

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

class ResultsSelectorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.items = []

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setIconSize(QtCore.QSize(256, 256))
        self.list_widget.setWordWrap(True)
        self.central_layout.addWidget(self.list_widget)

        self.setLayout(self.central_layout)

    def load_response(self, response):
        self.list_widget.clear()
        for item in response.get("items", []):
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
                else:
                    list_item = QtWidgets.QListWidgetItem(item_title, self.list_widget)

                self.list_widget.addItem(list_item)
                self.items.append(item_data)
            except KeyError:
                pass

class SelectorDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.songs = []
        self.song_index = 0
        self.load_songs()

        self.setWindowTitle("Select Results Dialog")
        self.setFixedSize(510, 700)

        self.central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.label_top = QtWidgets.QLabel("Loading...")
        self.central_layout.addWidget(self.label_top)

        self.results_selector = ResultsSelectorWidget()
        self.central_layout.addWidget(self.results_selector)

        self.btn_ok = QtWidgets.QPushButton("Ok")
        self.central_layout.addWidget(self.btn_ok)

        self.setCentralWidget(self.central_widget)

    def load_songs(self):
        try:
            songs_path = sys.argv[1]

            for path in Path(songs_path).rglob('*.mp3'):
                song_file = mutagen.File(path, easy=True)
                try:
                    self.songs.append({
                        "title": song_file["title"],
                        "artist": song_file["artist"]
                    })
                except KeyError:
                    print(
                        "Warning: skipped song file due to improper metadata: {}".format(path.relative_to(songs_path)))
        except IndexError:
            print("Please provide a songs path")

    def do_next_song(self):
        pass


# with open("out.json", "w") as f:
#     json.dump(youtube_search("akane sasu"), f)

with open("out.json", "r") as f:
    app = QtWidgets.QApplication(sys.argv)
    # window = ResultsSelectorWidget("Aimer - Akane Sasu", json.load(f))
    window = SelectorDialog()
    window.show()
    app.exec()
