import os
import subprocess
import logging
import time
import ffmpeg
from PIL import Image
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip

from src.generatecaption import apply_caption, fit_caption_to_frame

from .packages import check_dependency

__palfne = "palette.png"  # palette file name and extension
__capfne = "caption.png"  # caption file name and extension


# makes a gif from video using ffmpeg
def gif_from_video(in_vid: str, out_gif: str):
    logging.info("Converting video to gif...")

    st = time.time()
    ffmpeg.input(in_vid).filter("palettegen", reserve_transparent=1).output(
        __palfne
    ).run(quiet=True)
    logging.debug(f"Generated palette")

    ffmpeg.filter(
        [ffmpeg.input(in_vid), ffmpeg.input(__palfne)],
        "paletteuse",
        alpha_threshold=128,
    ).output(out_gif).run(quiet=True)
    et = time.time()

    logging.info(f"Converted video to gif in {et - st} seconds")


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    check_dependency("gifsicle")
    logging.info(f"Optimizing gif with compression scale {loss} and {colors} colors...")
    orig_size = os.stat(filepath).st_size
    st = time.time()
    sp = subprocess.run(
        [
            "gifsicle",
            "--no-comments",
            "-b",
            "-O8",
            f"--lossy={loss}",
            f"-k={colors}",
            filepath,
            "-w",
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    et = time.time()
    opti_size = os.stat(filepath).st_size

    logging.debug(sp.stdout)
    logging.info(
        f"Optimized gif in {et - st} seconds, files size reduced by { (orig_size - opti_size) / orig_size * 100 }%"
    )


def static_caption(in_img: str, out_img: str, caption_img: Image):
    with Image.open(in_img) as frame:
        caption_img = fit_caption_to_frame(frame.width, caption_img)
        captioned_img = apply_caption(frame, caption_img)
        captioned_img.save(out_img)


def motion_caption(in_vid: str, out_vid: str, caption_img: Image):
    logging.debug("Preparing video...")
    st = time.time()

    # prepare sources
    source_vid = VideoFileClip(in_vid)
    caption_img = fit_caption_to_frame(source_vid.w, caption_img)

    # canvas
    captioned_vid = ColorClip(
        (source_vid.w, source_vid.h + caption_img.height), color=(255, 255, 255)
    )

    # paste caption
    caption_img.save(__capfne)
    caption_clip = ImageClip(
        __capfne
    )  # we cannot pass it (?), gotta save and load apparently...
    captioned_vid = CompositeVideoClip(
        [captioned_vid, caption_clip.set_position(("center", "top"))]
    )

    # paste video
    captioned_vid = CompositeVideoClip(
        [captioned_vid, source_vid.set_pos(("center", "bottom"))]
    )

    # Export the final video
    captioned_vid = captioned_vid.set_duration(source_vid.duration)
    logging.info("Writing video...")
    captioned_vid.write_videofile(out_vid, logger=None)

    et = time.time()
    logging.info(f"Finished writing video in {et - st} seconds")
