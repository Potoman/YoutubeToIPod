import youtube_dl
import json
import time

class Song:

    youtubeId = -1
    title = ""
    url = ""

    def __init__(self, url):
        self.url = url
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

        self.title = a['title']
        self.youtubeId = a['id']

        time.sleep(5)

    def getFilePath(self):
        return self.title + "-" + self.youtubeId + ".mp3"


