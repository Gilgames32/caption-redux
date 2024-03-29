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

import emojiutil

def main():
    print_begin("Initializing directories")

    # project root
    base_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
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
    caption_id = generate_name(captiontext)
    while os.path.exists(tmp_rdir + caption_id):
        caption_id = generate_name(captiontext)
    tmp_rdir += caption_id
    ensure_folder(tmp_rdir)
    
    os.chdir(base_dir + tmp_rdir)
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
    
    
    
    
    if len(frames) <= 1:    
        caption_id += ".png"
        # todo: png optimization
        print_begin(f"Moving result to {out_rdir + caption_id}")
        os.replace(cwd + frames[0], base_dir + out_rdir + caption_id)
        print_check()
    
    else:
        caption_id += ".gif"
        # make gif
        gif_from_frames(caption_id, cwd, framenaming)
        # optimize gif
        gifsicle_optimize(cwd + caption_id)
    
        print_begin(f"Moving result to {out_rdir + caption_id}")
        os.replace(cwd + caption_id, base_dir + out_rdir + caption_id)
        print_check()
    
    print_begin("Cleaning up working directory")
    # clear_folder(cwd)
    os.rmdir(base_dir + tmp_rdir)
    print_check()
    
    print(f"Finished!")

if __name__ == '__main__':
    main()
