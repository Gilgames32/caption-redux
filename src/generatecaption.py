import logging
from emoji import is_emoji
from PIL import Image, ImageFont, ImageDraw

from .imgutil import get_width, get_height
from .emojiutil import get_emoji_image
from .textwraputil import weighted_textwrap
from . import config


# genereates the caption from the text
def generate_caption_image(rawtext: str) -> Image.Image:
    # setup font
    font = ImageFont.truetype(config.font_path, config.font_size)
    font_max_width = get_width(font, "x") * 2
    font_avg_height = get_height(font, "pÓ")
    font_max_height = font_avg_height * 2

    wrapped_lines, custom_emotes = weighted_textwrap(rawtext)

    logging.info("Rasterizing text...")
    line_images = []
    for line in wrapped_lines:
        # generate a large enough canvas
        line_image = Image.new(
            config.color_mode, (font_max_width * len(line), font_max_height)
        )
        line_draw = ImageDraw.Draw(line_image)

        x = 0
        for character in line:
            # emojis getting the special treatment
            if is_emoji(character):
                if character == "🦊":  # :3
                    character = custom_emotes.pop(0)

                emoji_image = get_emoji_image(character)
                emoji_image = emoji_image.resize((int(config.font_size),) * 2)

                line_image.paste(emoji_image, (x, font_avg_height // 2))

                x += emoji_image.width

            # the rest of the characters
            else:
                line_draw.text(
                    xy=(x, font_avg_height // 2),
                    text=character,
                    font=font,
                    fill=config.text_color,
                )
                x += get_width(font, character)

        # crop to the actual size
        line_image = line_image.crop(line_image.getbbox())
        logging.debug(f"Rasterized {line} to image, size: {line_image.size}")

        line_images.append(line_image)

    # the generous estimation of the maximum canvas size
    max_width = max([img.width for img in line_images])
    max_height = int((config.font_size + config.line_spacing) * len(line_images))

    # merge line images into one
    merged_lines = Image.new(config.color_mode, (max_width, max_height), (0,) * 4)
    logging.debug(f"Created merged canvas, size: {merged_lines.size}")

    y = 0
    for img in line_images:
        merged_lines.paste(img, ((merged_lines.width - img.width) // 2, int(y)), img)
        logging.debug(f"Pasted line image at y = {int(y)}")
        y += config.font_size + config.line_spacing

    merged_lines = merged_lines.crop(merged_lines.getbbox())
    logging.debug(f"Cropped merged canvas, size: {merged_lines.size}")

    # generate background
    caption = Image.new(
        config.color_mode,
        (
            # add padding
            max(merged_lines.width, config.minimum_line_width) + config.padding[0],
            merged_lines.height + config.padding[1],
        ),
        config.bg_color,
    )
    # paste merged lines in the middle
    caption.alpha_composite(
        merged_lines,
        (
            (caption.width - merged_lines.width) // 2,
            (caption.height - merged_lines.height) // 2,
        )
    )
    logging.debug(f"Added padding to caption, size: {caption.size}")

    logging.info("Rasterized text")

    return caption


# makes space at the top so we can put the caption there
def expand_image_canvas(
    frame: Image.Image, expand_top: int, color="#FFF"
) -> Image.Image:
    expanded = Image.new(frame.mode, (frame.width, frame.height + expand_top), color)
    expanded.paste(frame, (0, expand_top))
    logging.debug(f"Expanded image canvas from {frame.size} to {expanded.size}")
    return expanded


# resizes the caption so its width matches the frames
def fit_caption_to_frame(width: int, caption: Image.Image) -> Image.Image:
    caption = caption.resize(
        (width, int(float(caption.height) / caption.width * width))
    )
    logging.debug(f"Resized caption to match frame, size: {caption.size}")
    return caption


# merges the caption on the frame
def apply_caption(frame: Image.Image, caption: Image.Image) -> Image.Image:
    captioned = expand_image_canvas(frame, caption.height)
    captioned.paste(caption)
    logging.debug(f"Applied caption to frame")
    return captioned
