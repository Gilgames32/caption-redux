# Caption Redux

A GIF caption generator mimicing the iFunny caption style, popular on Discord, Reddit, and similar pits of the internet.

This project is a complete rewrite and extension of [kubinka0505's iFunny-Captions](https://github.com/kubinka0505/iFunny-Captions) project (archived).

## Feature list

- caption GIFs, videos and images
- options to configure fonts, emoji styles, colors, etc.
- support for Discord emotes (in `<:floraSmug:1112288234488201307>` format)
- optimizations for smaller filesizes (also configurable)
- supports both local and online files
- extra support for popular GIF hosting sites (Tenor, Giphy, etc.)
- option for transparent GIF captions



## Installation
For advanced users:
```bash
git clone https://github.com/Gilgames32/caption-redux.git
cd caption-redux
pip install -r requirements. txt
```
You **must** have [FFmpeg](https://www.ffmpeg.org/). [Gifsicle](https://www.lcdf.org/gifsicle/) is highly recommended but optional. [Pngcrush](https://pmt.sourceforge.io/pngcrush/) is negligible but also supported.

> [!IMPORTANT]  
> These packages must be added to the PATH for them to work.

*Dummy guide soon.*

## Usage
Run `main.py`. Optionally you can use arguments, see `-h`.
- `-i <image link>` path or direct URL to the image
- `-t <caption text>` the caption text
- `-a`: preserve GIF transparency (uses the legacy method, a bit slower) 
- `-g`: force GIF output (even if the input was a video or a static image)

Configuration guide (`config.json`):
- `safe_mode`: if enabled, captioning of local files will be disabled
- `loglevel`: for devs
- `text`
    - `font`: path to the font
    - `font_size`: font size
    - `wrap_width`: maximum amount of columns per line
    - `line_spacing`: spacing between lines
    - `padding`: padding of the text inside the caption
    - `minimum_line_width`: minimum line width
- `color`
    - `background`: the color of the background
    - `text`: the color of the text
- `emoji_style`: the style of the emojis, supported styles are `twitter`, `google`, `facebook` and `apple`
- `optimization`
    - `pngcrush`
        - `enabled`: if enabled and Pngcrush is installed, the result will be compressed
    - `gifsicle`
        - `enabled`: if enabled and Gifsicle is installed, the result will be compressed
        - `compression`: compression scale (bigger means more compression artifacts)
        - `colors`: number of colors (2-256)
        - `fps`: maximum framerate (if the input is lower than this, the original framerate will be used)
    - `video`
        - `enabled`: if enabled, the result will be compressed
        - `fps`: maximum framerate (if the input is lower than this, the original framerate will be used)
        - `bitrate`: the bitrate of the output video
        - `height`: the height of the output video (excluding the caption)

## Plans
> easier install

## Motivation

This project focuses on extended functionality, faster generation and cleaner code compared to it's alternatives (such as esmBot, the now archived repository or the official iFunny generator).

## Contribution
Contributions, pull requests, reviews, suggestions, issues and whatnot are welcome!


