import logging, unittest

import src.dly as dly

dly.LOGGER.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

dly.LOGGER.addHandler(ch)

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
        self.assertEqual(song.creator, "Eminem")
        self.assertEqual(song.alt_title, "Fall")
        self.assertEqual(song.get_id_file_name(), "MfTbHITdhEI.mp3")
        self.assertEqual(song.get_title_file_name(), "Eminem - Fall")
        dly.init_tag(song, True)
        dly.add_to_music(song)

    def test_basic_url(self):
        url = "https://www.youtube.com/watch?v=qfqA1sTKhmw"
        song = dly.download(url)
        self.assertEqual(song.creator, "Palmashow")
        self.assertEqual(song.alt_title, "Lartisto ft Lady Djadja 'trop de nanana'")
        self.assertEqual(song.get_id_file_name(), "qfqA1sTKhmw.mp3")
        self.assertEqual(song.get_title_file_name(), "Lartisto ft Lady Djadja 'trop de nanana' - Palmashow")
        dly.init_tag(song, True)
        dly.add_to_music(song)

if __name__ == '__main__':
    unittest.main()
