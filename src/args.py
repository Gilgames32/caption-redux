import logging
import argparse

captiontext: str = None
imgpath: str = None
parser = argparse.ArgumentParser(description="Caption Generator")

parser.add_argument("-i", "--image", help="url or path to the image", default="")
parser.add_argument("-t", "--text", help="caption text", default="")

def correctparse():
    args = parser.parse_args()
    logging.debug(f"Parsed arguments: {args}")

    # fill in arguments if none were given
    imgpath = args.image
    while imgpath == "":
        imgpath = input("Enter image path: ").strip()

    captiontext = args.text
    while captiontext == "":
        captiontext = input("Enter caption: ")
