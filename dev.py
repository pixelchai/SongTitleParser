import json
from lark import Lark

parser = Lark.open("title.lark", parser="earley")

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = []
for key, song in dataset.items():
    for result in song.get("results", []):
        try:
            results.append(result["title"])
        except KeyError:
            pass

print(parser.parse("Hi mate"))
