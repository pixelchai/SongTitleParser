from main import parse_simple
from youtube_title_parse import get_artist_title
import pyperclip as clip
import re
import time

last_clip = clip.paste()

def escape_picard(s):
    return s.replace(")", r"\)").replace("(", r"\(").replace("-", r"\-")

def unescape_picard(s):
    return s.replace(r"\)", ")").replace(r"\(", "(").replace(r"\-", "-")

def interpret_picard(picard_string):
    data = {}
    for match in re.finditer("(\\w+):\\(((?:[^\\\\)]|\\\\.)*)\\)", picard_string):
        key = match.group(1)
        value = unescape_picard(match.group(2))
        if key == "track":
            value = re.sub("-([^\"&?\\/\\s]{11})$", "", value)

            try:
                try:
                    artist, title = parse_simple(value)
                except:
                    artist, title = get_artist_title(value)

                data["artist"] = artist
                data["name"] = title
            except:
                pass

            data["track"] = value
        elif key != "tnum":
            data[key] = value

    ret = ""
    for key, value in data.items():
        ret += " {}:({})".format(key, escape_picard(value))
    return ret[1:]

while True:
    cur_clip = clip.paste()
    if cur_clip != last_clip:
        print("clip changed")
        new_clip = interpret_picard(cur_clip)
        clip.copy(new_clip)
        last_clip = new_clip
        print("updated clip")
    else:
        last_clip = cur_clip
    time.sleep(0.05)