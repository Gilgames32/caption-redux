from PIL import ImageFont
from typing import Tuple

def get_size(font: ImageFont.FreeTypeFont, text: str) -> Tuple[int, int]:
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom - top


def get_width(font: ImageFont.FreeTypeFont, text: str) -> int:
    left, top, right, bottom = font.getbbox(text)
    return right - left

def get_height(font: ImageFont.FreeTypeFont, text: str):
    left, top, right, bottom = font.getbbox(text)
    return bottom - top
