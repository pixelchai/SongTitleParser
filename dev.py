import json
import random
from main import parser, interpret_tree

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = [
"ずっと真夜中でいいのに。『ハゼ馳せる果てるまで』MV",
    "Beverly _ 尊い MUSIC VIDEO "
    # "Beverly _ 尊い MUSIC VIDEO 【作詞・作曲  - 岡崎体育】(3rd Album「INFINITY」収録)"
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
