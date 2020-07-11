from main import parse_simple
from youtube_title_parse import get_artist_title
import pyperclip as clip
import re
import time
import keyboard
import pyautogui as gui
import traceback

last_clip = clip.paste()

def escape_picard(s):
    return s.replace(")", r"\)").replace("(", r"\(").replace("-", r"\-").replace("[", r"\[").replace("]", r"\]")

def unescape_picard(s):
    return s.replace(r"\)", ")").replace(r"\(", "(").replace(r"\-", "-").replace(r"\[", "[").replace(r"\]", "]")

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
                    print("PARSE FAILED")
                    traceback.print_exc()
                    artist, title = get_artist_title(value)

                data["artist"] = artist
                data["name"] = title
            except:
                print("BOTH FAILED")
                traceback.print_exc()

            data["track"] = value
        elif key != "tnum":
            data[key] = value

    ret = ""
    for key, value in data.items():
        if value is not None:
            ret += " {}:({})".format(key, escape_picard(value))
    return ret[1:]

# while True:
#     cur_clip = clip.paste()
#     if cur_clip != last_clip:
#         print("clip changed")
#         new_clip = interpret_picard(cur_clip)
#         clip.copy(new_clip)
#         last_clip = new_clip
#         print("updated clip")
#     else:
#         last_clip = cur_clip
#     time.sleep(0.05)

while True:
    # wait until ctrl+p key
    keyboard.wait("ctrl+p")
    # do the thing
    gui.rightClick()
    time.sleep(0.2)
    gui.moveRel(10, 150)
    gui.click()
    time.sleep(0.3)
    keyboard.send("ctrl+a")
    time.sleep(0.2)
    keyboard.send("ctrl+c")
    time.sleep(0.2)
    new_clip = interpret_picard(clip.paste())
    clip.copy(new_clip)
    keyboard.send("ctrl+v")
    time.sleep(0.2)
    keyboard.send("enter")