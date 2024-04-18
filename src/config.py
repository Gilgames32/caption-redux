import json
import logging

config: dict
with open("config.json", "r") as f:
    config = json.load(f)

safe_mode = config["safe_mode"]

font_size = 100
font_path = config["text"]["font"]
text_wrap_width = 40
line_spacing = config["text"]["line_spacing"]
padding = config["text"]["padding"]
minimum_line_width = config["text"]["minimum_line_width"]

color_mode = "RGBA"
bg_color = config["color"]["background"]
text_color = config["color"]["text"]

emoji_style = config["emoji_style"]
if emoji_style not in ["twitter", "apple", "google", "facebook"]:
    raise ValueError("Invalid emoji style")


# TODO: there must be a better way to do this
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

# TODO: implement
force_gif = config["force_gif"]

# TODO: implement
aplha_gif = config["preserve_gif_transparency"]

