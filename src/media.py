import os
import requests
import logging
import ffmpeg

from . import config

__temp_source_filename = "source"   # temporary file name for the source
__framenaming = "frame_%05d.png"    # frame name template for ffmpeg


def check_media_site(url: str) -> str:
    if "https://" in url:
        if "tenor.com/view" in url:
            logging.info("Found media link in supported image hosting site")
            url = (
                requests.get(url)
                .text.split("contentUrl")[1]
                .replace("\\u002F", "/")
                .split('"')[2]
            )
        # TODO: add more

    logging.debug(f"Corrected url to {url}")
    return url


def determine_format(link: str) -> str:
    try:
        probe = ffmpeg.probe(link)
    except ffmpeg.Error as e:
        logging.error(f"FFmpeg error: {e.stderr}")
        raise ValueError("FFmpeg error")

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


def fetch_source(link: str, ext: str, work_dir: str, frames: bool) -> str:
    if os.path.exists(link):
        logging.debug(f"Local file detected at {link}")
        
        if config.safe_mode:
            logging.warning("Unable to access local files in safe mode")
            raise ValueError("Local files are disabled in safe mode")
        
        if frames:
            logging.info("Converting local file to frames...")
            # TODO: test
            frames_path = os.path.join(work_dir, __framenaming)
            ffmpeg.input(link).output(frames_path).overwrite_output().run(quiet=True)
            return frames_path
        
        return link
    
    elif link.startswith("https://"):
        if frames:
            logging.info("Fetching frames...")
            frames_path = os.path.join(work_dir, __framenaming)
            ffmpeg.input(link).output(frames_path).overwrite_output().run(quiet=True)
            return frames_path
        
        else:
            download_filename = __temp_source_filename + "." + (ext if ext != "gif" else "mp4")
            download_path = os.path.join(work_dir, download_filename)
            logging.info("Downloading media...")
            ffmpeg.input(link).output(download_path).run(quiet=True)
            return download_path
    
    else:
        logging.warning(f"Invalid source: {link}")
        raise ValueError("Invalid source link")
