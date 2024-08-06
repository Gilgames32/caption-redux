import json
import logging
import os

# project root
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/"

config: dict
with open(base_dir + "config.json", "r") as f:
    config = json.load(f)

safe_mode = config["safe_mode"]

font_size = 100
font_path = base_dir + config["text"]["font"]
text_wrap_width = config["text"]["wrap_width"]
line_spacing = config["text"]["line_spacing"]
padding = config["text"]["padding"]
minimum_line_width = config["text"]["minimum_line_width"]

color_mode = "RGBA"
bg_color = config["color"]["background"]
text_color = config["color"]["text"]

emoji_style = config["emoji_style"]
if emoji_style not in ["twitter", "apple", "google", "facebook"]:
    raise ValueError("Invalid emoji style")


__logdict = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}
loglevel = __logdict[config["loglevel"]]

gifsicle_enabled = config["optimization"]["gifsicle"]["enabled"]
gifsicle_compression = config["optimization"]["gifsicle"]["compression"]
gifsicle_colors = config["optimization"]["gifsicle"]["colors"]
gif_fps = config["optimization"]["gifsicle"]["fps"]

video_compress = config["optimization"]["video"]["enabled"]
video_bitrate = config["optimization"]["video"]["bitrate"]
video_fps = config["optimization"]["video"]["fps"]
video_height = config["optimization"]["video"]["height"]
