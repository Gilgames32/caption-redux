import os
from halo import Halo

from util import cwd, framenaming, silence_tools

palette = "palette.png"


# makes a gif from frames using ffmpeg
def gif_from_frames(fname: str, path: str = cwd, framenames: str = framenaming):
    spinner = Halo(text="Generating gif palette", spinner="dots")
    # generate palette
    os.system(
        f'ffmpeg -i "{path}{framenames}" -vf palettegen=reserve_transparent=1 -gifflags -offsetting "{path}{palette}" -y \
        {"-hide_banner -loglevel panic" if silence_tools else ""}'
    )
    spinner.stop_and_persist("✔")

    spinner = Halo(text="Generating gif", spinner="dots")
    # make gif
    os.system(
        f'ffmpeg -i "{path}{framenames}" -i "{path}{palette}" -lavfi paletteuse=alpha_threshold=128 "{path}{fname}" -y \
        {"-hide_banner -loglevel panic" if silence_tools else ""}'
    )
    spinner.stop_and_persist("✔")


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    spinner = Halo(text=f"Optimizing gif with compression scale {loss} and {colors} colors", spinner="dots")
    os.system(
        f'gifsicle --no-comments -b -O8 --lossy={loss} -k={colors} "{filepath}" \
            {"-w" if silence_tools else "-V"}'
    )
    spinner.stop_and_persist("✔")
