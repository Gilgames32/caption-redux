import logging
import argparse

captiontext: str = None
imgpath: str = None
parser = argparse.ArgumentParser(description="Caption Generator")

parser.add_argument("-i", "--image", help="url or path to the image", default="")
parser.add_argument("-t", "--text", help="caption text", default="")
parser.add_argument("-g", "--gif", help="force gif output", action=argparse.BooleanOptionalAction)
parser.add_argument("-a", "--alpha", help="preserve the alpha channel for gifs", action=argparse.BooleanOptionalAction)


def correctparse():
    global captiontext, imgpath, force_gif, gif_alpha
    args = parser.parse_args()
    logging.debug(f"Parsed arguments: {args}")
    
    force_gif = args.gif != None
    gif_alpha = args.alpha != None

    # fill in arguments if none were given
    imgpath = args.image
    while imgpath == "":
        imgpath = input("Enter image path: ").strip()

    captiontext = args.text
    while captiontext == "":
        captiontext = input("Enter caption: ")
