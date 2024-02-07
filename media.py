import os
import logging
import requests

from util import *


def get_media_link(url: str) -> str:
    if "//" in url:
        logging.info("Fetching from url...")
        if "tenor.com/view" in url:
            url = (
                requests.get(url)
                .text.split("contentUrl")[1]
                .replace("\\u002F", "/")
                .split('"')[2]
            )
        # more to come
    else:
        logging.info("Fetching from filesystem...")

    return url


def fetch_frames(imgpath: str, path: str = cwd, framename: str = framenaming):
    os.system(
        f'ffmpeg -i "{get_media_link(imgpath)}" "{path}{framename}" -y \
        {"-hide_banner -loglevel panic" if silence_tools else ""}'
    )
