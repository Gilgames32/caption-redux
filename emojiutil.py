import os
import requests
from PIL import Image
from emoji import demojize, is_emoji

from util import ensure_folder

emo_dir = "emojis/"

def get_emoji_image(emoji_character: str) -> Image.Image:
	if(is_emoji(emoji_character)):
		emoji_name = demojize(emoji_character, delimiters=("", ""))
	else:
		emoji_name = emoji_character[-20:-1]

	# check if we already have it downloaded
	if not os.path.exists(emo_dir + emoji_name + ".png"):
		if(is_emoji(emoji_character)):
			response = requests.get(f"https://emojicdn.elk.sh/{emoji_character}?style=twitter", stream=True)
		else:
			# ignoring animated discord emotes
			response = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_name}.png", stream=True)

		emoji_image = Image.open(response.raw).convert("RGBA")
		emoji_image.save(emo_dir + emoji_name + ".png", "png")

	return Image.open(emo_dir + emoji_name + ".png")
