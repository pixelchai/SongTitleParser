import unittest
from main import parser, interpret_tree

class TestParser(unittest.TestCase):
    def assertParse(self, raw_title, artist, title):
        self.assertTupleEqual(interpret_tree(parser.parse(raw_title)),
                              (artist, title))

    def test_examples(self):
        self.assertParse("Pixel - The Cool Song (Official Audio)",
                         "Pixel", "The Cool Song")
        self.assertParse("きて50 cent -- In Da Club (HQ) (HD)",
                         "きて50 cent", "In Da Club")
        self.assertParse("The Killers - Mr Brightside (Live at Glastonbury, UK 2019)",
                         "The Killers", "Mr Brightside")
        self.assertParse("[Eng/Indo/Lyric] Aimyon - 『She Used to Be Alive, Right?』 Ikite Itanda Yo Na 生きていたんだよな",
                         "Aimyon", "She Used to Be Alive, Right?")
        self.assertParse("Pixel - WowSong (CoolMovie OST) (EASY LYRICS)",
                         "Pixel", "WowSong")
        self.assertParse("猛独が襲う／初音ミク",
                         "初音ミク", "猛独が襲う")
        self.assertParse("ヨルシカ - 思想犯（OFFICIAL VIDEO）",
                         "ヨルシカ", "思想犯")
        self.assertParse("ずっと真夜中でいいのに。『ハゼ馳せる果てるまで』MV",
                         "ずっと真夜中でいいのに。", "ハゼ馳せる果てるまで")
        self.assertParse('"Humanoid" Music Video by Zutto Mayonaka de Ii no ni.',
                         "Zutto Mayonaka de Ii no ni.", "Humanoid")

if __name__ == '__main__':
    unittest.main(verbosity=2)