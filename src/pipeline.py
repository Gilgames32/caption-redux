import os
import logging
from PIL import Image

from .util import (
    cwd,
    framenaming,
    ensure_folder,
    clear_folder,
    generate_name,
)
from .media import fetch_frames
from .generatecaption import (
    generate_caption_image,
    fit_caption_to_frame,
    apply_caption,
)
from .makegif import gif_from_frames, gifsicle_optimize

from . import emojiutil
from .packages import check_dependency


def caption(caption_link: str, caption_text: str, silent=False) -> str:
    check_dependency("ffmpeg")
    check_dependency("gifsicle")

    
    logging.info("Initializing directories...")

    # project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/"
    os.chdir(base_dir)

    # tmp
    tmp_rdir = "tmp/"
    ensure_folder(tmp_rdir)

    # output
    out_rdir = "out/"
    ensure_folder(out_rdir)

    # emoji cache
    emojiutil.emo_dir = base_dir + "emojis/"
    ensure_folder(emojiutil.emo_dir)

    # generate unique folder
    caption_id = generate_name(caption_text)
    while os.path.exists(tmp_rdir + caption_id):
        caption_id = generate_name(caption_text)
    tmp_rdir += caption_id
    ensure_folder(tmp_rdir)

    os.chdir(base_dir + tmp_rdir)
    logging.debug(f"Working directory: {os.getcwd()}")

    fetch_frames(caption_link, cwd, framenaming)

    # sorted list of frames
    frames = sorted(
        [file for file in next(os.walk(cwd))[2] if file.endswith("png")], key=str
    )

    # generate caption image
    caption = generate_caption_image(caption_text)
    caption = fit_caption_to_frame(Image.open(cwd + frames[0]), caption)

    # apply to each frame
    logging.info("Applying caption to frames...")
    for frame in frames:
        frame_img = Image.open(cwd + frame)

        captioned = apply_caption(frame_img, caption)
        captioned.save(cwd + frame)

        frame_img.close()
    logging.info("Applied caption to frames") # TODO: time

    if len(frames) <= 1:
        logging.info("Single frame detected, saving as png")

        caption_id += ".png"
        # TODO: png optimization
        
        os.replace(cwd + frames[0], base_dir + out_rdir + caption_id)

    else:
        logging.info("Multiple frames detected, creating gif")
        
        caption_id += ".gif"
        # make gif
        gif_from_frames(caption_id, cwd, framenaming)
        # optimize gif
        gifsicle_optimize(cwd + caption_id)

        os.replace(cwd + caption_id, base_dir + out_rdir + caption_id)
    
    logging.info(f"Moved result to {out_rdir + caption_id}")

    logging.info("Cleaning up working directory...")
    clear_folder(cwd)
    os.chdir(base_dir)
    os.rmdir(tmp_rdir)

    return base_dir + out_rdir + caption_id
