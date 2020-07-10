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
        self.list_widget.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
        self.list_widget.setIconSize(QtCore.QSize(256, 256))
        self.list_widget.setWordWrap(True)
        self.central_layout.addWidget(self.list_widget)

        self.setLayout(self.central_layout)

    def load_response(self, response, load_image=False):
        self.list_widget.clear()
        for item in response.get("items", []):
            try:
                list_item = None

                item_data = {}
                item_id = item.get("id")
                item_snippet = item.get("snippet")

                # set id
                if item_id.get("kind") != "youtube#video":
                    continue
                item_data["id"] = item_id.get("videoId")

                # load title
                item_title = html.unescape(item_snippet.get("title", ""))
                item_data["title"] = item_title

                # load image
                thumbnail_url = item_snippet.get("thumbnails", {}).get("default", {}).get("url", None)
                if load_image and thumbnail_url is not None:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(requests.get(thumbnail_url).content)
                    list_item = QtWidgets.QListWidgetItem(QtGui.QIcon(pixmap), item_title, self.list_widget)
                    list_item.setFont(QtGui.QFont("Arial", 12))
                else:
                    list_item = QtWidgets.QListWidgetItem(item_title, self.list_widget)

                self.list_widget.addItem(list_item)
                self.items.append(item_data)
            except KeyError:
                pass

    def get_selected_items(self):
        for index in self.list_widget.selectedIndexes():
            yield self.items[index.row()]

class SelectorDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._msg = None

        self.songs = []
        self.song_index = 0
        self.load_songs()
        self.skip_done()

        self.setWindowTitle("Select Results Dialog")
        self.setFixedSize(510, 700)

        self.central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.check_load_thumbnails = QtWidgets.QCheckBox("Load thumbnails")
        self.check_load_thumbnails.setChecked(False)
        self.central_layout.addWidget(self.check_load_thumbnails)

        self.label_top = QtWidgets.QLabel("Loading...")
        self.label_top.setFont(QtGui.QFont("Arial", 12))
        self.label_top.setWordWrap(True)
        self.central_layout.addWidget(self.label_top)

        self.results_selector = ResultsSelectorWidget()
        self.central_layout.addWidget(self.results_selector)

        self.btn_ok = QtWidgets.QPushButton("Ok")
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.central_layout.addWidget(self.btn_ok)

        self.setCentralWidget(self.central_widget)

        self.do_song()

    def load_songs(self):
        try:
            songs_path = sys.argv[1]

            for path in Path(songs_path).rglob('*.mp3'):
                song_file = mutagen.File(path, easy=True)
                try:
                    self.songs.append({
                        "title": song_file["title"][0],
                        "artist": song_file["artist"][0]
                    })
                except KeyError:
                    print(
                        "Warning: skipped song file due to improper metadata: {}".format(path.relative_to(songs_path)))
        except IndexError:
            print("Please provide a songs path")

    def btn_ok_clicked(self):
        self.songs[self.song_index]["results"] = list(self.results_selector.get_selected_items())
        self.save_data()
        self.song_index += 1
        self.do_song()

    def skip_done(self):
        # skip songs already in out.json
        if not os.path.isfile("out.json"):
            return

        with open("out.json", "r") as f:
            data = json.load(f)

        buf = []
        for song in self.songs:
            key = "{} - {}".format(song["artist"], song["title"])
            if key in data:
                if "results" in data[key]:
                    continue
            buf.append(song)

        self.songs = buf

    def save_data(self):
        data = {}
        if os.path.isfile("out.json"):
            with open("out.json", "r") as f:
                data = json.load(f)

        for song in self.songs:
            key = "{} - {}".format(song["artist"], song["title"])
            data[key] = song

        with open("out.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Saved data!")

    def do_song(self):
        if self.song_index >= len(self.songs):
            print("Done!")
            self._msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Done", "Finished going through all of the songs.\nThe data has been stored in out.json")
            self._msg.setDetailedText(json.dumps(self.songs))
            self._msg.show()
            return
        else:
            song = self.songs[self.song_index]
            query = "{} - {}".format(song["artist"], song["title"])

            text_progress = "[{:03d}/{:03d} - {:00.00f}%]".format(self.song_index, len(self.songs),
                                                                  self.song_index / len(self.songs) * 100)
            self.setWindowTitle("Loading... " + text_progress)
            self.label_top.setText("Loading...")
            response = youtube_search(query)

            self.setWindowTitle("Selecting... " + text_progress)
            self.label_top.setText("Select the results which correspond to: <br>{}".format(query))
            self.results_selector.load_response(response, self.check_load_thumbnails.isChecked())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SelectorDialog()
    window.show()
    app.exec()
