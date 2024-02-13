import os
from PIL import Image
from tqdm import tqdm

from util import cwd, framenaming, ensure_folder, clear_folder, generate_name, print_check, print_begin
from args import imgpath, captiontext
from media import fetch_frames
from generatecaption import (
    generate_caption_image,
    fit_caption_to_frame,
    apply_caption,
)
from makegif import gif_from_frames, gifsicle_optimize

def main():
    # working directory
    base_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    tmp_dir = "tmp/"
    out_dir = "out/"
    
    print_begin("Initializing directories")
    ensure_folder(tmp_dir)
    ensure_folder(out_dir)
    clear_folder(tmp_dir)
    
    os.chdir(base_dir + tmp_dir)
    print_check()
    
    
    fetch_frames(imgpath, cwd, framenaming)
    
    # sorted list of frames
    frames = sorted(
        [file for file in next(os.walk(cwd))[2] if file.endswith("png")], key=str
    )
    
    
    # generate caption image
    caption = generate_caption_image(captiontext)
    caption = fit_caption_to_frame(Image.open(cwd + frames[0]), caption)
    
    
    # apply to each frame
    for i, frame in tqdm(enumerate(frames), desc="Applying caption", unit="frame"):
        frame_img = Image.open(cwd + frame)
    
        captioned = apply_caption(frame_img, caption)
        captioned.save(cwd + frame)
    
        frame_img.close()
    
    
    fname = generate_name(captiontext)
    
    if len(frames) <= 1:    
        fname += ".png"
        # todo: png optimization
        print_begin(f"Moving result to {out_dir + fname}")
        os.replace(cwd + frames[0], base_dir + out_dir + fname)
        print_check()
    
    else:
        fname += ".gif"
        # make gif
        gif_from_frames(fname, cwd, framenaming)
        # optimize gif
        gifsicle_optimize(cwd + fname)
    
        print_begin(f"Moving result to {out_dir + fname}")
        os.replace(cwd + fname, base_dir + out_dir + fname)
        print_check()
    
    print_begin("Cleaning up working directory")
    clear_folder(cwd)
    print_check()
    
    print(f"Finished!")

if __name__ == '__main__':
    main()
