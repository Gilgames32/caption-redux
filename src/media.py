import os
import requests
import logging
import ffmpeg

__infn = "source"  # input file name
__framenaming = "frame_%05d.png"


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


def determine_format(link: str) -> str:
    probe = ffmpeg.probe(link)

    if probe["format"]["format_name"] == "gif":
        logging.debug("Gif detected")
        return "gif"

    elif (
        "nb_frames" not in probe["streams"][0]
        or probe["streams"][0]["nb_frames"] == "1"
    ):
        logging.debug(
            "No frame count or single frame attribute detected, output will be static"
        )
        logging.info("Static image detected")
        return "png"

    else:
        logging.debug("Video detected")
        return "mp4"


def fetch_source(link: str, ext: str, frames: bool) -> str:
    # TODO: disable local files on servers
    if os.path.exists(link):
        logging.debug(f"Local file detected at {link}")
        if frames:
            logging.info("Converting local file to frames...")
            ffmpeg.input(link).output(__framenaming).overwrite_output().run(quiet=True)
            return __framenaming
        return link
    elif link.startswith("https://"):
        if frames:
            logging.info("Fetching frames...")
            ffmpeg.input(link).output(__framenaming).overwrite_output().run(quiet=True)
            return __framenaming
        else:
            dl = __infn + "." + (ext if ext != "gif" else "mp4")
            logging.info("Downloading media...")
            ffmpeg.input(link).output(dl).run(quiet=True)
            return dl
    else:
        logging.warning(f"Invalid source: {link}")
        raise ValueError("Invalid source link")
