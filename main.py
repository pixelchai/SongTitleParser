import re
import lark
from lark import Lark

parser = Lark.open("title.lark", parser="earley",  g_regex_flags=re.I)
def interpret_tree(tree: "lark.Tree"):
    artist_name = None
    song_title = None

    for tree in tree.iter_subtrees():
        if tree.data.startswith("artist_name"):
            artist_name = "/".join([str(x).strip() for x in tree.children])
        if tree.data.startswith("song_title"):
            song_title = str(tree.children[0]).strip()

    return artist_name, song_title