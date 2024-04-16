import os
import logging
import time
from PIL import Image
import ffmpeg
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip, ImageClip

from .util import ensure_folder, clear_folder, generate_name
from .media import get_media_link
from .generatecaption import generate_caption_image, fit_caption_to_frame, apply_caption
from .makegif import gifsicle_optimize

from . import emojiutil
from .packages import check_dependency


# temporary name constants
__infn = "source"   # input file name
__outfn = "result"  # output file name
__capfne = "caption.png" # caption file name and extension
__palfne = "palette.png" # palette file name and extension

def caption(caption_link: str, caption_text: str) -> str:
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

    # generate unique cwd
    caption_id = generate_name(caption_text)
    while os.path.exists(tmp_rdir + caption_id):
        caption_id = generate_name(caption_text)
    tmp_rdir += caption_id
    ensure_folder(tmp_rdir)

    # change cwd
    os.chdir(base_dir + tmp_rdir)
    logging.debug(f"Working directory: {os.getcwd()}")

    
    # check for supported sites
    caption_link = get_media_link(caption_link)

    # determine format
    ext: str
    probe = ffmpeg.probe(caption_link)
    if probe["format"]["format_name"] == "gif":
        ext = "gif"
        logging.debug("Gif detected")
    elif "nb_frames" not in probe["streams"][0] or probe["streams"][0]["nb_frames"] == '1':
        logging.debug("No frame count or single frame attribute detected, output will be static")
        logging.info("Static image detected")
        ext = "png"
    else:
        ext = "mp4"
        logging.debug("Video detected")

    
    # fetch source
    # TODO: disable local files on servers
    source_path: str
    if os.path.exists(caption_link):
        source_path = caption_link
        logging.debug(f"Local file detected at {source_path}")
    elif caption_link.startswith("https://"):
        source_path = __infn + "." + (ext if ext != "gif" else "mp4")
        ffmpeg.input(caption_link).output(source_path).run(quiet=True)
    else:
        logging.warning(f"Invalid source: {caption_link}")


    # generate caption image
    caption_img = generate_caption_image(caption_text)

    # apply caption
    output_fname = __outfn + "." + (ext if ext != "gif" else "mp4")
    logging.info("Applying caption...")
    if ext == "png":
        with Image.open(source_path) as frame:
            caption_img = fit_caption_to_frame(frame.width, caption_img)
            captioned_img = apply_caption(frame, caption_img)
            captioned_img.save(output_fname)
            # TODO: png optimization
    else:
        # prepare sources
        source_vid = VideoFileClip(source_path)
        caption_img = fit_caption_to_frame(source_vid.w, caption_img)

        # canvas
        captioned_vid = ColorClip((source_vid.w, source_vid.h + caption_img.height), color=(255, 255, 255))

        # paste caption
        caption_img.save(__capfne)
        caption_clip = ImageClip(__capfne)    # we cannot pass it (?), gotta save and load apparently...
        captioned_vid = CompositeVideoClip([captioned_vid, caption_clip.set_position(("center", "top"))])

        # paste video
        captioned_vid = CompositeVideoClip([captioned_vid, source_vid.set_pos(("center", "bottom"))])

        # Export the final video
        captioned_vid = captioned_vid.set_duration(source_vid.duration)
        logging.info("Writing video... (this may take a while)")
        st = time.time()
        captioned_vid.write_videofile(output_fname, logger=None)
        et = time.time()
        logging.info(f"Finished writing video in {et - st} seconds")
        
        if ext == "gif":
            # make gif from video
            logging.info("Converting video to gif...")
            output_gif_path = __outfn + ".gif"
            st = time.time()
            ffmpeg.input(output_fname).filter('palettegen', reserve_transparent=1).output(__palfne).run(quiet=True)
            logging.debug(f"Generated palette")
            ffmpeg.filter([ffmpeg.input(output_fname), ffmpeg.input(__palfne)], 'paletteuse', alpha_threshold=128).output(output_gif_path).run(quiet=True)
            et = time.time()
            logging.debug(f"Converted video to gif in {et - st} seconds")
            output_fname = output_gif_path

            # optimize gif
            gifsicle_optimize(output_fname)

    
    result_fname = caption_id + "." + ext
    os.replace(output_fname, base_dir + out_rdir + result_fname)
    logging.info(f"Moved result to {out_rdir + result_fname}")


    # TODO: cleanup on errors too
    logging.info("Cleaning up working directory...")
    clear_folder(tmp_rdir)
    os.chdir(base_dir)
    os.rmdir(tmp_rdir)


    return base_dir + out_rdir + result_fname
