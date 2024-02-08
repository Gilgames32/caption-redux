import os
import requests
from PIL import Image
from emoji import demojize

from util import ensure_folder

emo_dir = "emojis/"

def get_emoji_image(emoji_character: str) -> Image.Image:
	emoji_name = demojize(emoji_character, delimiters=("", ""))

	# check if we already have it downloaded
	ensure_folder(emo_dir)
	if not os.path.exists(emo_dir + emoji_name + ".png"):
		response = requests.get(f"https://emojicdn.elk.sh/{emoji_character}?style=twitter", stream=True)
		emoji_image = Image.open(response.raw).convert("RGBA")
		emoji_image.save(emo_dir + emoji_name + ".png", "png")

	return Image.open(emo_dir + emoji_name + ".png")
