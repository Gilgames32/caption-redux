import subprocess

from .util import cwd, framenaming, silence_tools, print_begin, print_check, print_tool

palette = "palette.png"


# makes a gif from frames using ffmpeg
def gif_from_frames(fname: str, path: str = cwd, framenames: str = framenaming):
    print_begin("Generating gif palette")
    # generate palette
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-vf", "palettegen=reserve_transparent=1", "-gifflags", "-offsetting", path + palette, "-y"], capture_output=True, check=True, text=True)
    print_tool(sp.stdout)

    print_check()

    print_begin("Generating gif")
    # make gif
    sp = subprocess.run(["ffmpeg", "-i", path + framenames, "-i", path + palette, "-lavfi", "paletteuse=alpha_threshold=128", path + fname, "-y"], capture_output=True, check=True, text=True)
    print_tool(sp.stdout)
    print_check()


# optimize gif using gifsicle and lossy compression
def gifsicle_optimize(filepath: str, loss: int = 200, colors: int = 256):
    print_begin(f"Optimizing gif with compression scale {loss} and {colors} colors")
    sp = subprocess.run(["gifsicle", "--no-comments", "-b", "-O8", f'--lossy={loss}', f'-k={colors}', filepath, "-w"], capture_output=True, check=True, text=True)
    print_tool(sp.stdout)
    print_check()
