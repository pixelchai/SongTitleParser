import json
import random
from lark import Lark
import re
from pprint import pprint

parser = Lark.open("title.lark", parser="earley",  g_regex_flags=re.I)

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = [
    "きて50 cent -- In Da Club (HQ) (HD)",
    "The Killers - Mr Brightside (Live at Glastonbury, UK 2019)",
    "The Killers - Mr Brightside (Live at Glastonbury, 2019, UK)",
    "Florence + The Machine - Times Like These - Live At Glastonbury 2015",
    "[Eng/Indo/Lyric] Aimyon - 『She Used to Be Alive, Right?』 Ikite Itanda Yo Na 生きていたんだよな",
    "Pixel - WowSong (woowh song) (EASY LYRICS)",
    "[EN/ESP] Aimyon - 『She Used to Be Alive, Right?』 Ikite Itanda Yo Na 生きていたんだよな",
    "猛独が襲う／初音ミク",
    "ヨルシカ - 思想犯（OFFICIAL VIDEO）",
    "ずっと真夜中でいいのに。『ハゼ馳せる果てるまで』MV",
]

if False:
    for key, song in dataset.items():
        for result in song.get("results", []):
            try:
                results.append(result["title"])
            except KeyError:
                pass

# random.shuffle(results)
for result in results[:100]:
    print(result)
    tree = parser.parse(result)
    print(tree.pretty("\t"))

tree = parser.parse("ヨルシカ - 思想犯（OFFICIAL VIDEO）")
print(tree)