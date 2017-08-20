import sys
import os
import re
import time
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from song import Song

libraryPath = os.environ['IPOD_LIBRARY_AUTO']

def main():
    print("enter")
    if len(sys.argv) < 2:
        sys.exit("No url pass by parameter.")
    print("enter")
    url = sys.argv[1]
    url = cleanUrl(url)
    artistFirst = sys.argv[2]
    print("Url load : " + url)
    song = download(url)
    filePath = song.getFilePath()
    initTag(filePath, song.title, artistFirst == "true" or artistFirst == "True")
    addToLibrary(filePath)
    return

def cleanUrl(url):
    return url.split("&list=")[0]

def download(url):
    return Song(url)

def initTag(filePath, title, artisteIsFirst):
    print("initTag > file : '" + filePath + "', title = '" + title + "'.")

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
    print("clean : '" + tag + "'")
    tag = re.sub(r'\[[^)]*\]', '', tag).strip()
    return tag

def setTag(filePath, **tags):
    print("setTag on file : '" + filePath + "'")
    mf = MP3(filePath, ID3=EasyID3)
    for key, value in tags.items():
        print("key : " + key + ", value : " + value)
        try:
            mf[key] = value
        except:
            print("No " + key)
    mf.save()
    print("setTag : ok")
    return;

def addToLibrary(filePath):
    print("Move file from : " + filePath + ", to " + libraryPath + "\\" + filePath)
    try:
        os.rename(filePath, libraryPath + "\\" + filePath)
    except OSError as e:
        print(e)
    time.sleep(5)
    return

if __name__ == "__main__":
    main()
