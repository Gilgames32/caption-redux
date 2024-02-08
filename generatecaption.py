from emoji import emojize, is_emoji
from textwrap import wrap
from PIL import Image, ImageFont, ImageDraw
from imgutil import get_width, get_height
from typing import List

from emojiutil import get_emoji_image
from util import print_begin, print_check


# setup font
max_width = 1000
font_size = max_width * 0.10
font_path = "Futura_Condensed_Extra_Bold.otf"
font = ImageFont.truetype(font_path, font_size)
# rough estimation
font_max_width = get_width(font, "x") * 2
font_avg_height = get_height(font, "pÓ")
font_max_height = font_avg_height * 2


# setup colors
color_mode = "RGBA"
text_color = "#000000"
background_color = "#FFFFFF"


# converts emojis and generates the wrapped lines
def generate_wrapped_lines(texto: str) -> List[str]:
    print_begin("Wrapping text")
    
    # convert emojis
    # texto = "when\n\nthe the the the the the the the the the the the y"
    texto = emojize(texto, variant="emoji_type", language="alias")
    texto = texto.strip()

    # wrap text
    lines = texto.split("\n")
    # im sorry
    # emojies kidna break wrapping !!!
    # todo: own wrapper
    wrapped_lines = sum(
        [wrap(line, width=22) if line != "" else list(" ") for line in lines], []
    )

    print_check()
    return wrapped_lines


# genereates the caption from the text
def generate_caption_image(wrapped_lines: List[str]) -> Image.Image:
    print_begin("Rasterizing text")
    
    # generate line images
    line_images = []
    for line in wrapped_lines:
        # generate a large enough canvas
        line_image = Image.new(
            color_mode, (font_max_width * len(line), font_max_height)
        )
        line_draw = ImageDraw.Draw(line_image)

        x = 0
        for character in line:
            # emojis getting the special treatment
            if is_emoji(character):
                emoji_image = get_emoji_image(character)
                emoji_image = emoji_image.resize((int(font_avg_height*0.8),) * 2)
		
                line_image.paste(emoji_image, (x, font_avg_height // 2))
                
                x += emoji_image.width

            # the rest of the characters
            else:
                line_draw.text(
                    xy=(x, font_avg_height // 2), text=character, font=font, fill=text_color
                )
                x += get_width(font, character)

        line_image = line_image.crop(line_image.getbbox())

        line_images.append(line_image)
        line_image.show()

    # merge line images onto one image
    merged_lines = Image.new(color_mode, (max_width, max_width * 5), (0,) * 4)

    y = 0
    for i, img in enumerate(line_images):
        # space between lines
        y += font_size * 1.28
        merged_lines.paste(img, ((merged_lines.width - img.width) // 2, int(y)), img)

    merged_lines = merged_lines.crop(merged_lines.getbbox())

    # generate background
    caption = Image.new(
        color_mode,
        (max_width, int(merged_lines.height + font_avg_height * 1.50)),
        background_color,
    )
    # paste in the middle
    caption.paste(
        merged_lines,
        (
            (caption.width - merged_lines.width) // 2,
            (caption.height - merged_lines.height) // 2,
        ),
        merged_lines,
    )
    caption.show()
    print_check()
    return caption


# makes space at the top so we can put the caption there
def expand_image_canvas(frame: Image.Image, expand_top: int, color="#FFF") -> Image.Image:
    expanded = Image.new(frame.mode, (frame.width, frame.height + expand_top), color)
    expanded.paste(frame, (0, expand_top))
    return expanded


# resizes the caption so its width matches the frames
def fit_caption_to_frame(frame: Image.Image, caption: Image.Image) -> Image.Image:
    print_begin("Resizing caption")
    
    caption = caption.resize(
        (frame.width, int(float(caption.height) / caption.width * frame.width))
    )
    
    print_check()
    return caption


# merges the caption on the frame
def apply_caption(frame: Image.Image, caption: Image.Image) -> Image.Image:
    captioned = expand_image_canvas(frame, caption.height)
    captioned.paste(caption)
    return captioned
