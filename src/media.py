import os
import requests

from .util import cwd, framenaming, silence_tools, print_begin, print_check


def get_media_link(url: str) -> str:
    if "//" in url:
        if "tenor.com/view" in url:
            url = (
                requests.get(url)
                .text.split("contentUrl")[1]
                .replace("\\u002F", "/")
                .split('"')[2]
            )
        # more to come

    return url


def fetch_frames(imgpath: str, path: str = cwd, framename: str = framenaming):
    print_begin("Fetching frames")
    os.system(
        f'ffmpeg -i "{get_media_link(imgpath)}" "{path}{framename}" -y \
        {"-hide_banner -loglevel panic" if silence_tools else ""}'
    )
    print_check()
