import os
import logging

from . import emojiutil
from .packages import check_dependency
from .generatecaption import generate_caption_image
from .util import ensure_folder, clear_folder, generate_name
from .media import determine_format, fetch_source, get_media_link
from .makegif import gif_from_video, gifsicle_optimize, motion_caption, static_caption
from . import config

__outfn = "result"  # output file name


def caption(caption_link: str, caption_text: str) -> str:
    check_dependency("ffmpeg")

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

    # generate unique cwd
    caption_id = generate_name(caption_text)
    while os.path.exists(tmp_rdir + caption_id):
        caption_id = generate_name(caption_text)
    tmp_rdir += caption_id
    ensure_folder(tmp_rdir)

    # change cwd
    os.chdir(base_dir + tmp_rdir)
    logging.debug(f"Working directory: {os.getcwd()}")

    logging.info("Fetching media...")

    # check for supported sites
    caption_link = get_media_link(caption_link)

    ext = determine_format(caption_link)
    source_path = fetch_source(caption_link, ext)

    # generate caption image
    caption_img = generate_caption_image(caption_text)

    # apply caption
    output_fname = __outfn + "." + (ext if ext != "gif" else "mp4")
    logging.info("Applying caption...")
    if ext == "png":
        static_caption(source_path, output_fname, caption_img)
        # TODO: png optimization

    else:
        motion_caption(source_path, output_fname, caption_img)

        if ext == "gif":
            output_gif_path = __outfn + ".gif"
            gif_from_video(output_fname, output_gif_path)
            output_fname = output_gif_path

            # optimize gif
            if config.gifsicle_enabled:
                gifsicle_optimize(output_fname, config.gifsicle_compression, config.gifsicle_colors)

    # TODO: not sure if 1000 or 1024 is the proper conversion here
    # TODO: round
    logging.info(f"Result is {os.path.getsize(output_fname) / 1024} KB")

    result_fname = caption_id + "." + ext
    os.replace(output_fname, base_dir + out_rdir + result_fname)
    logging.info(f"Moved result to {out_rdir + result_fname}")

    # TODO: cleanup on errors too
    logging.info("Cleaning up working directory...")
    clear_folder("./")
    os.chdir(base_dir)
    os.rmdir(tmp_rdir)

    return base_dir + out_rdir + result_fname
