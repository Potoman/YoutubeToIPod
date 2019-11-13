import os, re, sys
import logging, traceback
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from shutil import copyfile
from pathlib import Path

from .song import Song


LOGGER = logging.getLogger('YoutubeToIpod')


def get_itunes_root_path():
    return os.path.join(Path.home(), "Music", "iTunes", "iTunes Media")


def get_itunes_music_youtube():
    return os.path.join(get_itunes_root_path(), "MUSIC", "Youtube")


def get_itunes_music_automatic_add():
    return os.path.join(get_itunes_root_path(), "Ajouter automatiquement à iTunes")


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
        url = clean_url(url)
        LOGGER.debug("url cleared : " + url)
        artiste_is_first = sys.argv[2]
        LOGGER.info("artistFirst : " + artiste_is_first)
        song = download(url)
        init_tag(song,  True if artiste_is_first else False)
        add_to_library(song)
    except Exception as e:
        LOGGER.error(traceback.format_exc())


def clean_url(url):
    return url.split("&list=")[0]


def download(url):
    return Song(url)


def init_tag(song, artiste_is_first):
    if song.get_title():
        init_tag_from_song(song)
    else:
        init_tag_from_title(song, artiste_is_first)


def init_tag_from_song(song):
    LOGGER.info('init_tag_from_song > song : ' + song)
    set_tag(song, title=song.get_title(), artist=song.get_author())
    return 0


def init_tag_from_title(song, artiste_is_first):
    LOGGER.info('init_tag_from_title > song : ' + song)

    title = clean_tag(song.get_title().strip())
    title = title.replace(":", "-")
    title = title.replace("--", "-")
    title = title.replace("lyrics", "")
    title = title.replace("\"", "'")

    tab_title = title.split("-")

    size = len(tab_title)

    if size == 0:
        set_tag(song, title=clean_tag(title.strip()))
    elif size == 1:
        set_tag(song, title=clean_tag(title.strip()))
    elif size >= 2:
        index_artiste = 0 if artiste_is_first else 1
        index_title = 1 if index_artiste == 0 else 0
        set_tag(song, artist=clean_tag(tab_title[index_artiste]), title=clean_tag(tab_title[index_title]))
    else:
        return -1
    return 0;


def clean_tag(tag):
    tag = re.sub(r'\([^)]*\)', '', tag).strip()
    LOGGER.info("clean : '" + tag + "'")
    tag = re.sub(r'\[[^)]*\]', '', tag).strip()
    return tag


def set_tag(song, **tags):
    file_path = song.get_id_file_name()
    LOGGER.info("set_tag on file : '" + file_path + "'")
    mf = MP3(file_path, ID3=EasyID3)
    for key, value in tags.items():
        LOGGER.debug("key : " + key + ", value : " + value)
        try:
            mf[key] = value
        except:
            print("No " + key)
    mf.save()
    LOGGER.debug("set_tag : ok")


def add_to_library(song):
    try:
        add_to_music(song)
        file_path = song.get_title_file_name()
        LOGGER.debug("Move file '" + file_path + "' to " + get_itunes_music_automatic_add())
        copyfile(os.path.join(get_itunes_music_youtube(), file_path), os.path.join(get_itunes_music_automatic_add(), file_path))
        LOGGER.debug("Move file '" + file_path + "' to " + get_itunes_music_automatic_add())
    except Exception as e:
        LOGGER.error(e)


def add_to_music(song):
    try:
        file_path = song.get_id_file_name()
        LOGGER.debug("Move file '" + file_path + "' to " + get_itunes_music_youtube())
        try:
            os.makedirs(get_itunes_music_youtube())
        except FileExistsError as fee:
            # directory already exists
            LOGGER.debug(fee)
            pass
        os.rename(file_path, os.path.join(get_itunes_music_youtube(), song.get_title_file_name()))
    except OSError as e:
        LOGGER.error(e)


if __name__ == "__main__":
    main()
