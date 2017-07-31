import youtube_dl
import sys
import os
import json
import re
import time
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

libraryPath = os.environ['IPOD_LIBRARY_AUTO']

def main():
    if len(sys.argv) < 2:
        sys.exit("No url pass by parameter.")

    url = sys.argv[1]

    print("Url load : " + url)

    download(url)

    return

def download(url):

    ydl_opts = {
        #'outtmpl': 'tmp.webm',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    ydl_opts_info = {
        'outtmpl': 'tmp.webm',
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        result = ydl.extract_info(url, download=True)

    if 'entries' in result:
        video = result['entries'][0]
    else:
        video = result

    array = json.dumps(video)
    a = json.loads(array)

    filePath = a['title'] + "-" + a['id'] + ".mp3"
    print("file : " + filePath)

    title = a['title']
    print(title)

    tabTitle = title.split("-")

    size = len(tabTitle)

    if size == 0:
        setTag(filePath, cleanTag(title.strip()))
    elif size == 1:
        setTag(filePath, title.strip())
    elif size >= 2:
        setTag(filePath, artist=cleanTag(tabTitle[0]), title=cleanTag(tabTitle[1]))
    else:
        return -1

    addToLibrary(filePath)

    return 0;

def cleanTag(tag):
    tag = re.sub(r'\([^)]*\)', '', tag).strip()
    print("clean : '" + tag + "'")
    tag = re.sub(r'\[[^)]*\]', '', tag).strip()
    return tag

def setTag(filePath, **tags):

    print("setTag on file : '" + filePath + "'")

    mf = MP3(filePath, ID3=EasyID3)

    size = len(tags)

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
