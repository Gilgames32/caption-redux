import os

from util import *

palette = "palette.png"

# makes a gif from frames using ffmpeg
def gif_from_frames(fname: str, path: str = cwd , framenames: str = framenaming):
    # generate palette
    os.system(
        f'ffmpeg -i "{path}{framenames}" -vf palettegen=reserve_transparent=1 -gifflags -offsetting "{path}{palette}" -y \
        {"-hide_banner -loglevel panic" if not devmode else ""}'
    )

    # make gif
    os.system(
        f'ffmpeg -i "{path}{framenames}" -i "{path}{palette}" -lavfi paletteuse=alpha_threshold=128 "{path}{fname}" -y \
        {"-hide_banner -loglevel panic" if not devmode else ""}'
    )


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    os.system(f'gifsicle --no-comments -b -O8 --lossy={loss} -k={colors} "{filepath}" \
            {"-V" if devmode else "-w"}')

