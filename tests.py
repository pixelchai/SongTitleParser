import unittest
from main import parser, interpret_tree

class TestParser(unittest.TestCase):
    def assertParse(self, raw_title, artist, title):
        artist_out, title_out = interpret_tree(parser.parse(raw_title))

        if artist is not None:
            self.assertEqual(artist, artist_out)

        if title is not None:
            self.assertEqual(title, title_out)

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
                         "ずっと真夜中でいいのに。", "ハゼ馳せる果てるまで")  # non-latin [non-latin] => not translation
        self.assertParse('"Humanoid" Music Video by Zutto Mayonaka de Ii no ni.',
                         "Zutto Mayonaka de Ii no ni.", "Humanoid")
        self.assertParse("Nice Song -- The Band feat. PixelZerg (Live at Glastonbury, 2019) 『OFFICIAL VIDEO』",
                         "The Band/PixelZerg", "Nice Song")
        self.assertParse("The Band feat. PixelZerg -- Nice Song (Live at Glastonbury, 2019) 『OFFICIAL VIDEO』",
                         "The Band/PixelZerg", "Nice Song")
        # self.assertParse("'Only One King' (feat. Jung Youth) _ Produced by Tommee Profitt",
        #                  "Jung Youth", "Only One King")
        self.assertParse("[cover]優しい人_yama",
                         "優しい人", "yama")  # special underscore, meta_unam prefix
        self.assertParse("[EngSub] Asu no Yozora Shoukaihan [Yuaru]",
                         "Yuaru", "Asu no Yozora Shoukaihan")  # Name [Artist] format
        # Name [translation] (and no artist) tends to be more common than Name [artist] so favour the former
        # especially if 'name' and 'translation' are from different alphabets
        self.assertParse("Anata no Yoru ga Akeru Made [あなたの夜が明けるまで] Lyrics",
                         None, "Anata no Yoru ga Akeru Made")
        self.assertParse("Word", None, "Word") # word on its own => song title
        self.assertParse("ayiko - Teichopsia (ft. Shoko)", "ayiko", "Teichopsia")
        self.assertParse("Beverly -- 尊い MUSIC VIDEO [cover]", "Beverly", "尊い")  # <Artist> - <name> <meta_unam> special case
        self.assertParse("Songname. / Mafumafu 【Sang it】", "Mafumafu", "Songname.")  # rev_sep with meta
if __name__ == '__main__':
    unittest.main(verbosity=2)