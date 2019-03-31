import youtube_dl
import time
import logging


class Song:

    def __init__(self, url):
        self.url = url
        ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        ydl = youtube_dl.YoutubeDL(ydl_opts)

        with ydl:
            result = ydl.extract_info(url, download=True)

        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        logging.debug(result)

        self.id = video['id']
        self.title = video['title']
        self.alt_title = video['alt_title']
        self.creator = video['creator']

        time.sleep(5)

    def get_file_name(self):
        return self.title + ".mp3"
