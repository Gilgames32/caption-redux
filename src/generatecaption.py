import logging
from emoji import is_emoji
from PIL import Image, ImageFont, ImageDraw

from .imgutil import get_width, get_height
from .emojiutil import get_emoji_image
from .textwraputil import weighted_textwrap


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


# genereates the caption from the text
def generate_caption_image(rawtext: str) -> Image.Image:
    wrapped_lines, custom_emotes = weighted_textwrap(rawtext)

    logging.info("Rasterizing text...")
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
                if character == "🦊":   # :3
                    character = custom_emotes.pop(0)

                emoji_image = get_emoji_image(character)
                emoji_image = emoji_image.resize((int(font_size),) * 2)

                line_image.paste(emoji_image, (x, font_avg_height // 2))

                x += emoji_image.width

            # the rest of the characters
            else:
                line_draw.text(
                    xy=(x, font_avg_height // 2),
                    text=character,
                    font=font,
                    fill=text_color,
                )
                x += get_width(font, character)

        line_image = line_image.crop(line_image.getbbox())
        logging.debug(f"Rasterized {line} to image, size: {line_image.size}")

        line_images.append(line_image)

    # merge line images onto one image
    merged_lines = Image.new(color_mode, (max_width, max_width * 5), (0,) * 4)
    logging.debug(f"Created merged canvas, size: {merged_lines.size}")

    y = 0
    for img in line_images:
        # space between lines
        y += font_size * 1.28
        merged_lines.paste(img, ((merged_lines.width - img.width) // 2, int(y)), img)
        logging.debug(f"Pasted line image at y = {int(y)}")

    merged_lines = merged_lines.crop(merged_lines.getbbox())
    logging.debug(f"Cropped merged canvas, size: {merged_lines.size}")

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
    logging.debug(f"Added padding to caption, size: {caption.size}")

    logging.info("Rasterized text")

    return caption


# makes space at the top so we can put the caption there
def expand_image_canvas(frame: Image.Image, expand_top: int, color="#FFF") -> Image.Image:
    expanded = Image.new(frame.mode, (frame.width, frame.height + expand_top), color)
    expanded.paste(frame, (0, expand_top))
    logging.debug(f"Expanded image canvas from {frame.size} to {expanded.size}")
    return expanded


# resizes the caption so its width matches the frames
def fit_caption_to_frame(frame: Image.Image, caption: Image.Image) -> Image.Image:
    caption = caption.resize(
        (frame.width, int(float(caption.height) / caption.width * frame.width))
    )
    logging.debug(f"Resized caption to match frame, size: {caption.size}")
    return caption


# merges the caption on the frame
def apply_caption(frame: Image.Image, caption: Image.Image) -> Image.Image:
    captioned = expand_image_canvas(frame, caption.height)
    captioned.paste(caption)
    logging.debug(f"Applied caption to frame")
    return captioned
