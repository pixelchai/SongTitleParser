import re
import lark
from lark import Lark

parser = Lark.open("title.lark", parser="earley",  g_regex_flags=re.I)
def interpret_tree(tree: "lark.Tree"):
    artist_name = None
    song_title = None

    for tree in tree.iter_subtrees_topdown():
        if tree.data.startswith("artist_name"):
            # if artist_name_ft inside artist_name, artist_name will be overwritten (because topdown)
            artist_name = "/".join([str(x).strip() for x in tree.children])
        if tree.data.startswith("song_title"):
            # only return first child of song_title because parsing is experimental
            song_title = str(tree.children[0]).strip()

    return artist_name, song_title