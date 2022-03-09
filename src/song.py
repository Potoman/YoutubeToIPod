import youtube_dl
import logging


class Song:

    def __init__(self, url: str):
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

        # Looking for the artist :
        if 'artist' in video and video['artist'] is not None:
            self.creator = video['artist']
        elif 'creator' in video and video['creator'] is not None:
            self.creator = video['creator']
        else:
            self.creator = 'Unknown'

        # Looking for the track title :
        if 'track' in video and video['track'] is not None:
            self.title = video['track']
        elif 'alt_title' in video and video['alt_title'] is not None:
            self.title = video['alt_title']
        else:
            self.title = 'Unknown'

        if self.creator is None:
            self.creator = input("No creator is detected. Please write one :")
        if self.title is None:
            self.title = input("No title is detected. Please write one :")

    def get_id_file_name(self) -> str:
        return self.id + ".mp3"

    def get_title_file_name(self) -> str:
        return (self.get_author() + " - " + self.get_title() + ".mp3")\
            .replace("\\", " ")\
            .replace("/", " ")\
            .replace(":", " ")\
            .replace("*", " ")\
            .replace("?", " ")\
            .replace("\"", "")\
            .replace("<", " ")\
            .replace(">", " ")\
            .replace("|", " ")

    def get_title(self) -> str:
        return self.title

    def get_author(self) -> str:
        return self.creator

    def __str__(self):
        return "song : id = '" + self.id \
               + "', title = '" + self.title \
               + "', creator = '" + self.creator + "'."

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
