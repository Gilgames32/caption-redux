import os
import subprocess
import logging
import time
import ffmpeg
from PIL import Image
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip

from .generatecaption import apply_caption, fit_caption_to_frame
from .config import Config

from .packages import check_dependency

__palette_filename = "palette.png"  # palette file name and extension
__caption_filename = "caption.png"  # caption file name and extension

# makes a gif from frames using ffmpeg
def gif_from_frames(in_frames: str, out_gif: str, work_dir: str):
    logging.info("Generating gif palette...")
    st = time.time()
    palette_path = os.path.join(work_dir, __palette_filename)
    ffmpeg.input(in_frames).filter("palettegen", reserve_transparent=1).output(palette_path).run(quiet=True)
    logging.debug(f"Generated palette")

    logging.info("Generating gif...")
    ffmpeg.filter(
        [ffmpeg.input(in_frames), ffmpeg.input(palette_path)],
        "paletteuse",
        alpha_threshold=128,
    ).output(out_gif).run(quiet=True)
    et = time.time()
    logging.info(f"Converted frames to gif in {et - st} seconds")


# makes a gif from video using ffmpeg
def convert_to_gif(in_vid: str, out_gif: str, work_dir: str):
    logging.info("Converting video to gif...")

    palette_path = os.path.join(work_dir, __palette_filename)

    st = time.time()
    ffmpeg.input(in_vid).filter("palettegen", reserve_transparent=1).output(
        palette_path
    ).run(quiet=True)
    logging.debug(f"Generated palette")

    ffmpeg.filter(
        [ffmpeg.input(in_vid), ffmpeg.input(palette_path)],
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


def motion_caption(in_vid: str, out_vid: str, caption_img: Image, work_dir: str, config: Config, is_gif: bool):
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
    caption_path = os.path.join(work_dir, __caption_filename)
    # we cannot pass it (?), gotta save and load apparently...
    caption_img.save(caption_path)
    caption_clip = ImageClip(caption_path)
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

    # compression is pointless for gifs
    if is_gif and config.gifsicle_enabled:
        captioned_vid.write_videofile(out_vid, fps=min(config.gif_fps, source_vid.fps), logger=None)
    
    # compress video if enabled
    elif not is_gif and config.video_compression_enabled:
        if source_vid.h > config.video_height:
            captioned_vid.resize(height=config.video_height)
        captioned_vid.write_videofile(out_vid, logger=None, threads=4, 
                                      bitrate=config.video_bitrate,
                                      fps=min(config.video_fps, source_vid.fps))
    else:
        captioned_vid.write_videofile(out_vid, logger=None, threads=4)
    

    et = time.time()
    logging.info(f"Finished writing video in {et - st} seconds")


# the old frame-by-frame captioning method
def legacy_caption(in_frames, out_gif: str, caption_img: Image, work_dir: str):
    # sorted list of frames
    frames = sorted(
        [os.path.join(work_dir, file) for file in next(os.walk(work_dir))[2] if file.endswith("png")], key=str
    )

    # fit caption to frame
    first_frame = Image.open(frames[0])
    caption_img = fit_caption_to_frame(first_frame.width, caption_img)
    first_frame.close()

    # apply to each frame
    logging.info(f"Applying caption to {len(frames)} frames...")
    st = time.time()
    for frame in frames:
        frame_img = Image.open(frame)
        captioned = apply_caption(frame_img, caption_img)
        captioned.save(frame)
        frame_img.close()

    et = time.time()
    logging.info(f"Applied caption to {len(frames)} frames in {et - st} seconds")

    # convert to gif
    gif_from_frames(in_frames, out_gif, work_dir)

def pngcrush_optimize(filepath: str):
    check_dependency("pngcrush")
    logging.info("Optimizing png with pngcrush...")
    orig_size = os.stat(filepath).st_size
    st = time.time()
    sp = subprocess.run(
        ["pngcrush", "-ow", filepath], capture_output=True, check=True, text=True
    )
    et = time.time()
    opti_size = os.stat(filepath).st_size

    logging.debug(sp.stdout)
    logging.info(
        f"Optimized png in {et - st} seconds, files size reduced by { (orig_size - opti_size) / orig_size * 100 }%"
    )