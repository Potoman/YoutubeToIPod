import youtube_dl
import os
import logging


class Song:

    def __init__(self, url):
        self.url = url
        ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(id)s.%(ext)s',
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

    def get_id_file_name(self):
        return self.id + ".mp3"

    def get_title_file_name(self):
        return self.title.replace("\"", "").replace("/", " ").replace("?", " ") + ".mp3"

    def __str__(self):
        return "song : id = '" + self.id \
               + "', title = '" + self.title \
               + "', alt_title = '" + self.alt_title \
               + "', creator = '" + self.creator + "'."

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
