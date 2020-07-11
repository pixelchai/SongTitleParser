import json
import unicodedata

def char_embed(char: str):
    """
    Number from 0-16 representing class
    """
    ret = 0
    # space
    if char.isspace(): return ret
    else: ret += 1

    list_classes = [
        '"', # quote
        "'", # apostrophe or quote
        "+&", # plus or ampersand
        "/／", # slash
        ".。", # dot/fullstop
        ",", # comma
    ]

    for char_class in list_classes:
        if char in char_class:
            return ret
        else:
            ret += 1

    cat = unicodedata.category(char)
    if char in "([『「（【［<{" or cat == "Ps": return ret
    else: ret += 1
    if char in ")]』」）】］>}" or cat == "Pe": return ret
    else: ret += 1
    if char in "-__—" or cat == "Pd": return ret
    else: ret += 1
    if cat.startswith("P"): return ret
    else: ret += 1

    if cat == "Lu": return ret
    else: ret += 1
    if cat == "Ll": return ret
    else: ret += 1
    # NB: no explicit class for Lo
    if cat.startswith("L"): return ret
    else: ret += 1

    if cat.startswith("N"): return ret
    else: ret += 1
    if cat.startswith("S"): return ret
    else: ret += 1

    return ret

with open("dataset/out.json", "r") as f:
    dataset = json.load(f)

results = [
]

for key, song in dataset.items():
    for result in song.get("results", []):
        try:
            results.append(result["title"])
        except KeyError:
            pass

for result in results:
    for char in result:
        embed = char_embed(char)
        if embed is None:
            print(char)

print(char_embed(u"​"))