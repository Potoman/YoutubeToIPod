import os, re, sys
import logging, traceback
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from shutil import copyfile
from pathlib import Path
import urllib.parse as urllibparse
import time
from win10toast import ToastNotifier

from .song import Song


LOGGER = logging.getLogger('YoutubeToIpod')


def get_itunes_root_path() -> str:
    return os.path.join(Path.home(), "Music", "iTunes", "iTunes Media")


def get_itunes_music_youtube() -> str:
    return os.path.join(get_itunes_root_path(), "MUSIC", "Youtube")


def get_itunes_music_automatic_add() -> str:
    return os.path.join(get_itunes_root_path(), "Ajouter automatiquement à iTunes")


def clean_file(file_path) -> None:
    if os.path.isfile(file_path):
        os.remove(file_path)
        LOGGER.debug("File deleted : " + file_path)


def main():
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
    try:
        url = clean_url(url)
        LOGGER.debug("url cleared : " + url)
        song = download(url)
        init_tag(song)
        add_to_library(song)
        toast_success(song)
    except Exception:
        toast_error(url)
        LOGGER.error(traceback.format_exc())
        time.sleep(10)


def url_to_id(url: str) -> str:
    parsed = urllibparse.urlparse(url)
    return urllibparse.parse_qs(parsed.query)['v'][0]


def id_to_url(id: str) -> str:
    return "https://www.youtube.com/watch?v=" + id


def clean_url(url: str) -> str:
    return id_to_url(url_to_id(url))


def download(url: str) -> Song:
    return Song(url)


def init_tag(song: Song) -> None:
    LOGGER.info('init_tag_from_song > song : ' + song)
    set_tag(song, title=song.get_title(), artist=song.get_author())


def clean_tag(tag: str) -> str:
    tag = re.sub(r'\([^)]*\)', '', tag).strip()
    LOGGER.info("clean : '" + tag + "'")
    tag = re.sub(r'\[[^)]*\]', '', tag).strip()
    return tag


def set_tag(song: Song, **tags) -> None:
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


def add_to_library(song: Song) -> None:
    try:
        add_to_music(song)
        file_path = song.get_title_file_name()
        dest = os.path.join(get_itunes_music_automatic_add(), file_path)
        LOGGER.debug("add_to_library : clean file '" + dest)
        clean_file(dest)
        src = os.path.join(get_itunes_music_youtube(), file_path)
        LOGGER.debug("add_to_library : move file '" + src + "' to " + dest)
        copyfile(src, dest)
    except Exception as e:
        LOGGER.error("add_to_library " + str(e))
        raise e


def add_to_music(song: Song) -> None:
    try:
        file_path = song.get_id_file_name()
        try:
            os.makedirs(get_itunes_music_youtube())
        except FileExistsError as fee:
            # directory already exists
            LOGGER.debug(fee)
            pass
        dest = os.path.join(get_itunes_music_youtube(), song.get_title_file_name())
        LOGGER.debug("add_to_music : clean file '" + dest)
        clean_file(dest)
        LOGGER.debug("add_to_music : move file '" + file_path + "' to " + dest)
        os.rename(file_path, dest)
    except OSError as e:
        LOGGER.error("add_to_music " + str(e))
        raise e


def toast_success(song: Song) -> None:
    toaster = ToastNotifier()
    toaster.show_toast("YoutubeToIPod : Success", "The song '" + song.get_title() + "' by '" + song.get_author() + "' is download.")


def toast_error(url: str) -> None:
    toaster = ToastNotifier()
    toaster.show_toast("YoutubeToIPod : Error", "The song at url '" + url + "' fail to be downloaded.")


if __name__ == "__main__":
    main()
