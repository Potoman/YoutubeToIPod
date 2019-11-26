import logging, unittest
import unittest.mock as mock

import src.dly as dly

dly.LOGGER.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

dly.LOGGER.addHandler(ch)


def song_basic_generator():
    song_basic = ["Palmashow", "Trop de nanana"]
    for i in song_basic:
        yield i

song_basic = song_basic_generator()

def mock_input(prompt):
    return next(song_basic)

class TestStringMethods(unittest.TestCase):

    def test_cleanUrl_noListInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        url = urlPart0
        self.assertEqual(urlPart0, dly.clean_url(url))
        print("Ok with no list.")

    def test_cleanUrl_listInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        urlPart1 = "tata"
        url = urlPart0 + "&list=" + urlPart1
        self.assertEqual(urlPart0, dly.clean_url(url))
        print("Ok with list.")

    def test_vevo_url(self):
        url = "https://www.youtube.com/watch?v=MfTbHITdhEI"
        song = dly.download(url)
        self.assertEqual(song.get_author(), "Eminem")
        self.assertEqual(song.get_title(), "Fall")
        self.assertEqual(song.get_id_file_name(), "MfTbHITdhEI.mp3")
        self.assertEqual(song.get_title_file_name(), "Eminem - Fall.mp3")
        dly.init_tag(song)
        dly.add_to_music(song)

    def test_basic_url(self):
        url = "https://www.youtube.com/watch?v=qfqA1sTKhmw"
        with mock.patch('builtins.input', mock_input):
            song = dly.download(url)
            self.assertEqual(song.get_author(), "Palmashow")
            self.assertEqual(song.get_title(), "Trop de nanana")
            self.assertEqual(song.get_id_file_name(), "qfqA1sTKhmw.mp3")
            self.assertEqual(song.get_title_file_name(), "Palmashow - Trop de nanana.mp3")
            dly.init_tag(song)
            dly.add_to_music(song)

    def test_song_with_wrong_character(self):
        url = "https://www.youtube.com/watch?v=FwUrbzh2qzA"
        song = dly.download(url)
        dly.init_tag(song)
        dly.add_to_music(song)
        self.assertEqual(song.get_author(), "Kool Shen / Akhenaton / Lino / Disiz la Peste / Nekfeu / Sneazzy / Sadek / Still Fresh / S.Pri Noir / Taïro / Nessbeal / Soprano / Dry")
        self.assertEqual(song.get_title(), "Marche")
        self.assertEqual(song.get_id_file_name(), "FwUrbzh2qzA.mp3")
        self.assertEqual(song.get_title_file_name(), "Kool Shen   Akhenaton   Lino   Disiz la Peste   Nekfeu   Sneazzy   Sadek   Still Fresh   S.Pri Noir   Taïro   Nessbeal   Soprano   Dry - Marche.mp3")

    def test_complexe_url(self):
        id = "7SwfwMxUVGI"
        clean_url = "https://www.youtube.com/watch?v=" + id
        bad_url = clean_url + "&list=" + id + "&start_radio=1"
        self.assertEqual(dly.url_to_id(bad_url), id)
        self.assertEqual(dly.id_to_url(id), clean_url)
        self.assertEqual(dly.clean_url(bad_url), clean_url)

if __name__ == '__main__':
    unittest.main()
