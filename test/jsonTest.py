import youtube_dl
import sys
import json
import unittest

import dly
from dly import cleanUrl

class TestStringMethods(unittest.TestCase):

    def test_cleanUrl_noListInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        url = urlPart0
        self.assertEqual(urlPart0, cleanUrl(url))
        print("Ok with no list.")

    def test_cleanUrl_listInUrl(self):
        urlPart0 = "https://www.youtube.com/watch?v=toto"
        urlPart1 = "tata"
        url = urlPart0 + "&list=" + urlPart1
        self.assertEqual(urlPart0, cleanUrl(url))
        print("Ok with list.")

if __name__ == '__main__':
    unittest.main()
