import os
import logging

from . import emojiutil
from .packages import check_dependency
from .generatecaption import generate_caption_image
from .util import ensure_folder, clear_folder, generate_name
from .media import determine_format, fetch_source, get_media_link
from .makegif import convert_to_gif, gifsicle_optimize, motion_caption, static_caption, legacy_caption
from . import config
from .config import base_dir

# TODO: move this to conf lol
__outfn = "result"  # output file name


def caption(caption_link: str, caption_text: str, force_gif=False, gif_alpha=False) -> str:
    check_dependency("ffmpeg")

    logging.info("Initializing directories...")

    # project root
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
    source_path = fetch_source(caption_link, ext, gif_alpha and ext == "gif")

    # generate caption image
    caption_img = generate_caption_image(caption_text)

    # apply caption
    logging.info("Applying caption...")
    output_fname = __outfn + "." + ext

    if ext == "gif" and gif_alpha:
        legacy_caption(source_path, output_fname, caption_img)
    elif ext == "png":
        static_caption(source_path, output_fname, caption_img)
        if force_gif:
            logging.info("Converting png to gif...")
            convert_to_gif(output_fname, __outfn + ".gif")
            output_fname = __outfn + ".gif"
            ext = "gif"
    else:
        temp_outname = __outfn + ".mp4"
        motion_caption(source_path, temp_outname, caption_img)

        if ext == "gif" or force_gif:
            convert_to_gif(temp_outname, output_fname)

    # optimize
    # TODO: png optimization
    if ext == "gif" and config.gifsicle_enabled:
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
