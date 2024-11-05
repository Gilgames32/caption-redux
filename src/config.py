import json
import logging
import os

# project root
# FIXME
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/"

class Config:
    # dont tamper
    color_mode = "RGBA"

    emoji_dir = "emojis/"
    tmp_dir = "tmp/"
    out_dir = "out/"

    def __init__(self, args, config_path = "config.json"):
        with open(config_path, "r") as f:
            config = json.load(f)

        # from args
        self.image_path = args.image
        self.caption_text = args.text
        self.force_gif = args.gif
        self.gif_alpha = args.alpha

        # from config
        self.safe_mode = config.get("safe_mode", True)
        self.loglevel = config.get("loglevel", "info").upper()

        self.font_path = config.get("text", {}).get("font", "fonts/OpenSans-Regular.ttf")
        self.font_size = config.get("text", {}).get("font_size", 100)
        self.text_wrap_width = config.get("text", {}).get("wrap_width", 22)
        self.line_spacing = config.get("text", {}).get("line_spacing", 28)
        self.text_padding = config.get("text", {}).get("padding", [150, 150])
        self.minimum_line_width = config.get("text", {}).get("minimum_line_width", 800)
        
        self.bg_color = config.get("color", {}).get("background", "#FFFFFF")
        self.text_color = config.get("color", {}).get("text", "#000000")

        self.emoji_style = config.get("emoji_style", "twitter")

        self.pngcrush_enabled = config.get("optimization", {}).get("pngcrush", {}).get("enabled", False)
        self.gifsicle_enabled = config.get("optimization", {}).get("gifsicle", {}).get("enabled", False)
        self.gifsicle_compression = config.get("optimization", {}).get("gifsicle", {}).get("compression", 200)
        self.gifsicle_colors = config.get("optimization", {}).get("gifsicle", {}).get("colors", 256)
        self.gif_fps = config.get("optimization", {}).get("gifsicle", {}).get("fps", 30)
        self.video_compression = config.get("optimization", {}).get("video", {}).get("enabled", False)
        self.video_fps = config.get("optimization", {}).get("video", {}).get("fps", 30)
        self.video_bitrate = config.get("optimization", {}).get("video", {}).get("bitrate", "1000k")
        self.video_height = config.get("optimization", {}).get("video", {}).get("height", 480)

        self.validate()

    def validate(self):
        if self.emoji_style not in ["twitter", "apple", "google", "facebook"]:
            raise ValueError("Invalid emoji style")
        if self.loglevel not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid loglevel")
        if self.video_bitrate[-1] not in ["k", "M"] and not self.video_bitrate[:-1].isdigit():
            raise ValueError("Invalid bitrate")
