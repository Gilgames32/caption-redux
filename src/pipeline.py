import os
import logging

from .packages import check_dependency
from .generatecaption import generate_caption_image
from .util import ensure_folder, clear_folder, generate_name
from .media import determine_format, fetch_source
from .mediasites import process_url
from .makegif import convert_to_gif, gifsicle_optimize, motion_caption, static_caption, legacy_caption, pngcrush_optimize
from .config import Config


__tmp_result_name = "result"    # temporary output file name


def caption(config: Config) -> str:    
    setup_environment()
    unique_id, unique_dir = make_unique_dir(config.caption_text)

    config.image_path = process_url(config.image_path)

    try:
        source_ext = determine_format(config.image_path)
        legacy_gif_method = source_ext == "gif" and config.gif_alpha
        source_path = fetch_source(config.image_path, source_ext, unique_dir, legacy_gif_method, config.safe_mode)

        caption_img = generate_caption_image(config)

        output_fname = apply_caption(config, source_path, caption_img, source_ext, unique_dir, legacy_gif_method)
        optimize(config, output_fname)

        result_path = move_result(output_fname, unique_id)

    except Exception as e:
        raise e
    finally:
        logging.info("Cleaning up working directory...")
        clear_folder(unique_dir)
        os.rmdir(unique_dir)

    return result_path


def setup_environment():
    logging.debug("Setting up working directories")

    check_dependency("ffmpeg")
    ensure_folder(Config.tmp_dir)
    ensure_folder(Config.emoji_dir)
    ensure_folder(Config.out_dir)


def make_unique_dir(text: str) -> tuple[str, str]:
    logging.debug("Generating unique working directory")

    while os.path.exists(unique_dir := (Config.tmp_dir + (unique_id := generate_name(text)))):
        pass

    ensure_folder(unique_dir)

    logging.debug(f"Unique directory: {unique_dir}")
    return unique_id, unique_dir


def apply_caption(config: Config, source_path: str, caption_img: str, ext: str, work_dir: str, legacy_gif_method: bool = False):
    logging.info("Applying caption...")

    output_path = os.path.join(work_dir, __tmp_result_name + "." + ext)

    if legacy_gif_method:
        legacy_caption(source_path, output_path, caption_img, work_dir)
    elif ext == "png":
        static_caption(source_path, output_path, caption_img)
        if config.force_gif:
            logging.info("Converting png to gif...")
            new_output_path = os.path.join(work_dir, __tmp_result_name + ".gif")
            convert_to_gif(output_path, new_output_path, work_dir)
            output_path = new_output_path
            ext = "gif"
    else:
        temp_output_path = os.path.join(work_dir, __tmp_result_name + ".mp4")
        motion_caption(source_path, temp_output_path, caption_img, work_dir, config, ext == "gif")

        if ext == "gif" or config.force_gif:
            convert_to_gif(temp_output_path, output_path, work_dir)

    return output_path

def optimize(config: Config, filepath: str):
    ext = filepath.split(".")[-1]
    if ext == "png" and config.pngcrush_enabled:
        pngcrush_optimize(filepath)
    elif ext == "gif" and config.gifsicle_enabled:
        gifsicle_optimize(filepath, config.gifsicle_compression, config.gifsicle_colors)

    logging.info(f"Result is {round(os.path.getsize(filepath) / 1024, 2)} KB")


def move_result(output_fname: str, unique_id: str):
    output_ext = output_fname.split(".")[-1]
    result_fname = unique_id + "." + output_ext

    result_path = os.path.join(Config.out_dir, result_fname)
    os.replace(output_fname, result_path)

    logging.info(f"Moved result to {result_path}")

    return result_path
