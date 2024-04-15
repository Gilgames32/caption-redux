import subprocess
import logging

from .util import cwd, framenaming

palette = "palette.png"


# makes a gif from frames using ffmpeg
def gif_from_frames(fname: str, path: str = cwd, framenames: str = framenaming):
    logging.info("Generating gif palette...")
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-vf", "palettegen=reserve_transparent=1", "-gifflags", "-offsetting", path + palette, "-y"], capture_output=True, check=True, text=True)
    logging.debug(sp.stdout)
    logging.info("Generated gif palette") # TODO: show time

    logging.info("Generating gif...")
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-i", path + palette, "-lavfi", "paletteuse=alpha_threshold=128", path + fname, "-y"], capture_output=True, check=True, text=True)
    logging.debug(sp.stdout)
    logging.info("Generated gif") # TODO: show time


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    logging.info(f"Optimizing gif with compression scale {loss} and {colors} colors...")
    sp = subprocess.run(["gifsicle", "--no-comments", "-b", "-O8", f'--lossy={loss}', f'-k={colors}', filepath, "-w"], capture_output=True, check=True, text=True)
    logging.debug(sp.stdout)
    logging.info("Optimized gif") # TODO: show reduce rate and time
