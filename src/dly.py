import sys
import os
import re
import time
import logging, traceback
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from song import Song

libraryPath = os.environ['IPOD_LIBRARY_AUTO']
LOGGER = logging.getLogger('YoutubeToIpod')

def main():
    try:
        LOGGER.setLevel(logging.DEBUG)

        fh = logging.FileHandler('log.txt')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        LOGGER.addHandler(fh)
        LOGGER.addHandler(ch)

        LOGGER.info("dly-main")
        if len(sys.argv) < 2:
            LOGGER.error("No url pass by parameter.")
            sys.exit("")
        else:
            LOGGER.info("ok for parameter size.")
        url = sys.argv[1]
        LOGGER.debug("url : " + url)
        url = cleanUrl(url)
        LOGGER.debug("url cleared : " + url)
        artistFirst = sys.argv[2]
        LOGGER.info("artistFirst : " + artistFirst)
        song = download(url)
        filePath = song.getFilePath()
        initTag(filePath, song.title, artistFirst == "true" or artistFirst == "True")
        addToLibrary(filePath)
    except Exception as e:
        LOGGER.error(traceback.format_exc())

def cleanUrl(url):
    return url.split("&list=")[0]

def download(url):
    return Song(url)

def initTag(filePath, title, artisteIsFirst):
    LOGGER.info("initTag > file : '" + filePath + "', title = '" + title + "'.")

    title = cleanTag(title.strip())
    title = title.replace(":", "-")
    title = title.replace("--", "-")
    title = title.replace("lyrics", "")

    tabTitle = title.split("-")

    size = len(tabTitle)

    if size == 0:
        setTag(filePath, title=cleanTag(title.strip()))
    elif size == 1:
        setTag(filePath, title=cleanTag(title.strip()))
    elif size >= 2:
        indexArtiste = 0 if artisteIsFirst else 1
        indexTitle = 1 if indexArtiste == 0 else 0
        setTag(filePath, artist=cleanTag(tabTitle[indexArtiste]), title=cleanTag(tabTitle[indexTitle]))
    else:
        return -1
    return 0;

def cleanTag(tag):
    tag = re.sub(r'\([^)]*\)', '', tag).strip()
    LOGGER.info("clean : '" + tag + "'")
    tag = re.sub(r'\[[^)]*\]', '', tag).strip()
    return tag

def setTag(filePath, **tags):
    LOGGER.info("setTag on file : '" + filePath + "'")
    mf = MP3(filePath, ID3=EasyID3)
    for key, value in tags.items():
        LOGGER.debug("key : " + key + ", value : " + value)
        try:
            mf[key] = value
        except:
            print("No " + key)
    mf.save()
    LOGGER.debug("setTag : ok")

def addToLibrary(filePath):
    LOGGER.debug("Move file from : " + filePath + ", to " + libraryPath + "\\" + filePath)
    try:
        os.rename(filePath, libraryPath + "\\" + filePath)
    except OSError as e:
        print(e)

if __name__ == "__main__":
    main()
