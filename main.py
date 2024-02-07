import os
import logging

logging.basicConfig(level=logging.INFO)

from PIL import Image

from util import cwd, framenaming, ensure_folder, clear_folder, generate_name
from args import imgpath, captiontext
from media import fetch_frames
from generatecaption import (
    generate_caption_image,
    generate_wrapped_lines,
    fit_caption_to_frame,
    apply_caption,
)
from makegif import gif_from_frames, gifsicle_optimize


# working directory
base_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
tmp_dir = "tmp/"
out_dir = "out/"

logging.info(f"Initializing directories...")
ensure_folder(tmp_dir)
ensure_folder(out_dir)
clear_folder(tmp_dir)

os.chdir(base_dir + tmp_dir)


logging.info(f"Fetching frames...")
fetch_frames(imgpath, cwd, framenaming)

# sorted list of frames
frames = sorted(
    [file for file in next(os.walk(cwd))[2] if file.endswith("png")], key=str
)


# generate caption image
caption = generate_caption_image(generate_wrapped_lines(captiontext))
caption = fit_caption_to_frame(Image.open(cwd + frames[0]), caption)


# apply to each frame
for i, frame in enumerate(frames):
    logging.info(f"Applying caption to frame {i+1}/{len(frames)}...")
    frame_img = Image.open(cwd + frame)

    captioned = apply_caption(frame_img, caption)
    captioned.save(cwd + frame)

    frame_img.close()


fname = generate_name(captiontext) + ".gif"

# make gif
gif_from_frames(fname, cwd, framenaming)
gifsicle_optimize(cwd + fname)

logging.info(f"Moving result to {out_dir + fname}...")
os.replace(cwd + fname, base_dir + out_dir + fname)
logging.info("Cleaning up working directory...")
clear_folder(cwd)

logging.info(f"Finished!")
