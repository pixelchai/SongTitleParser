import json
import random
from lark import Lark
from pprint import pprint

parser = Lark.open("title.lark", parser="earley")

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = [
    "50 cent - In Da Club (HQ)"
]

if False:
    for key, song in dataset.items():
        for result in song.get("results", []):
            try:
                results.append(result["title"])
            except KeyError:
                pass

random.shuffle(results)
for result in results[:10]:
    tree = parser.parse(result)
    print("{:50.50}".format(result))
    print(tree.pretty("\t"))