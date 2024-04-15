import os
import subprocess
import logging
import time

from .util import cwd, framenaming

palette = "palette.png"


# makes a gif from frames using ffmpeg
def gif_from_frames(fname: str, path: str = cwd, framenames: str = framenaming):
    logging.info("Generating gif palette...")
    st = time.time()
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-vf", "palettegen=reserve_transparent=1", "-gifflags", "-offsetting", path + palette, "-y"], capture_output=True, check=True, text=True)
    et = time.time()
    logging.debug(sp.stdout)
    logging.info(f"Generated gif palette in {et - st} seconds")

    logging.info("Generating gif...")
    st = time.time()
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-i", path + palette, "-lavfi", "paletteuse=alpha_threshold=128", path + fname, "-y"], capture_output=True, check=True, text=True)
    et = time.time()
    logging.debug(sp.stdout)
    logging.info(f"Generated gif in {et - st} seconds")


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    logging.info(f"Optimizing gif with compression scale {loss} and {colors} colors...")
    orig_size = os.stat(filepath).st_size
    st = time.time()
    sp = subprocess.run(["gifsicle", "--no-comments", "-b", "-O8", f'--lossy={loss}', f'-k={colors}', filepath, "-w"], capture_output=True, check=True, text=True)
    et = time.time()
    opti_size = os.stat(filepath).st_size
    
    logging.debug(sp.stdout)
    logging.info(f"Optimized gif in {et - st} seconds, files size reduced by { (orig_size - opti_size) / orig_size * 100 }%")
