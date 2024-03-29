import re
from textwrap import wrap
from emoji import is_emoji, emojize
from typing import List


def add_emoji_weight(text: str) -> str:
    # how tf would one write regex for emojis lol
    weighted_text = ""
    for c in text:
        if is_emoji(c):
            weighted_text += c * 2
        weighted_text += c
    return weighted_text


def remove_emoji_weight(lines: List[str]) -> List[str]:
    ci = 0
    for i, line in enumerate(lines):
        # yes i hear you crying
        unweighted_text = ""
        while ci < len(line):
            character = line[ci]
            unweighted_text += character
            ci += 3 if is_emoji(character) else 1
        ci -= len(line)  # if it split a triple, we carry ci to the next line
        lines[i] = unweighted_text

    return lines


def weighted_textwrap(text: str):
    # convert emojis
    text = emojize(text.strip(), variant="emoji_type", language="alias")

    # regex for emotes and the fox emoji
    dc_emote_pattern = r"<:[^:]+:\d+>|<a:[^:]+:\d+>|🦊"

    # replace emotes with placeholder fox
    emotes = re.findall(dc_emote_pattern, text)
    text = re.sub(dc_emote_pattern, "🦊", text)

    # add weight to emojis
    text = add_emoji_weight(text)

    # handle explicit linebreaks
    lines = text.split(r"\n")

    # lol
    wrapped_lines = sum(
        [wrap(line, width=22) if line != "" else list(" ") for line in lines], []
    )

    # remove weight from text
    wrapped_lines = remove_emoji_weight(wrapped_lines)

    return wrapped_lines, emotes
