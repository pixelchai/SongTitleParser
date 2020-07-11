import json
import random
from main import parser, interpret_tree

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = [
    'Nice Song -- The Band feat. PixelZerg (Live at Glastonbury, 2019) 『OFFICIAL VIDEO』',
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
    print(interpret_tree(tree))
    # print(tree)


# tree = parser.parse("ヨルシカ - 思想犯（OFFICIAL VIDEO）")
# print(tree)
