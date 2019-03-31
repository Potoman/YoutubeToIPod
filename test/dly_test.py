import unittest

import dly
from dly import clean_url


class TestStringMethods(unittest.TestCase):

    def test_cleanUrl_noListInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        url = urlPart0
        self.assertEqual(urlPart0, clean_url(url))
        print("Ok with no list.")

    def test_cleanUrl_listInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        urlPart1 = "tata"
        url = urlPart0 + "&list=" + urlPart1
        self.assertEqual(urlPart0, clean_url(url))
        print("Ok with list.")

    def test_vevo_url(self):
        url = "https://www.youtube.com/watch?v=MfTbHITdhEI"
        song = dly.download(url)
        dly.init_tag(song, True)
        dly.add_to_music(song)

    def test_basic_url(self):
        url = "https://www.youtube.com/watch?v=qfqA1sTKhmw"
        song = dly.download(url)
        dly.init_tag(song, True)
        dly.add_to_music(song)

if __name__ == '__main__':
    unittest.main()
