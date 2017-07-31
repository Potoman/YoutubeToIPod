import youtube_dl
import sys
import json


ydl_opts = {
    #'outtmpl': 'tmp.webm',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        #'preferredquality': '192',
    }],
}

ydl_opts_info = {
    'outtmpl': 'tmp.webm',
}

url = ""

print("Url load : " + url)

ydl = youtube_dl.YoutubeDL(ydl_opts)

with ydl:
    result = ydl.extract_info(url, download=False)


if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

array = json.dumps(video)
a = json.loads(array)

title = a['title']

print(title)

tabTitle = title.split("-")

size = len(tabTitle)

print(size)



# video_url = video['url']
# print(video_url)


