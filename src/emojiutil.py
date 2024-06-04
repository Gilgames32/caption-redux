import os
import io
import re
import requests
import logging
from PIL import Image
from emoji import demojize, is_emoji

from . import config

emo_dir = "emojis/"


def get_emoji_image(emoji_character: str) -> Image.Image:
    if is_emoji(emoji_character):
        emoji_name = config.emoji_style + "_" + demojize(emoji_character, delimiters=("", ""))
        logging.debug(f"Demojized {emoji_character} to {emoji_name}")
    else:
        emoji_name = re.search(":[\d]+>", emoji_character).group()[1:-1]
        logging.debug(f"Extracted {emoji_name} from discord emote {emoji_character}")

    emoji_path = emo_dir + emoji_name + ".png"
    # check if its in cache
    if not os.path.exists(emoji_path):
        logging.debug(f"Emoji {emoji_name} not found in cache, downloading...")
        if is_emoji(emoji_character):
            response = requests.get(
                f"https://emojicdn.elk.sh/{emoji_character}?style={config.emoji_style}", stream=True
            )
            logging.debug(f"Downloaded {emoji_character} from emojicdn, style: {config.emoji_style}")
        else:
            # ignoring animated discord emotes
            response = requests.get(
                f"https://cdn.discordapp.com/emojis/{emoji_name}.png", stream=True
            )
            logging.debug(f"Downloaded {emoji_name} from discord cdn")

        emoji_image = Image.open(io.BytesIO(response.content)).convert("RGBA")
        emoji_image.save(emoji_path, "png")
        logging.debug(f"Saved emoji to {emoji_path}")
    else:
        logging.debug(f"Found {emoji_name} in cache")

    return Image.open(emoji_path)
