import os
import requests
import logging
import subprocess

from .util import cwd, framenaming


def get_media_link(url: str) -> str:
    if "https://" in url:
        if "tenor.com/view" in url:
            logging.info("Found media link in supported image hosting site")
            url = (
                requests.get(url)
                .text.split("contentUrl")[1]
                .replace("\\u002F", "/")
                .split('"')[2]
            )
        # more to come

    return url


def fetch_frames(imgpath: str, path: str = cwd, framename: str = framenaming):
    logging.info(f"Fetching frames from {imgpath}...")
    sp = subprocess.run(["ffmpeg", "-i", get_media_link(imgpath), path + framename, "-y"], capture_output=True, check=True, text=True)
    logging.debug(sp.stdout)
    logging.info(f"Fetched {len(os.listdir(path))} frames")
