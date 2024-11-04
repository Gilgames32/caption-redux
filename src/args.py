import logging
from argparse import ArgumentParser, Namespace, BooleanOptionalAction

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Caption Redux - Caption Generator")
    parser.add_argument("-i", "--image", help="URL or path to the image")
    parser.add_argument("-t", "--text", help="Caption text")
    parser.add_argument("-g", "--gif", help="Force GIF output", action=BooleanOptionalAction)
    parser.add_argument("-a", "--alpha", help="Preserve the alpha channel for GIFs", action=BooleanOptionalAction)

    args = parser.parse_args()
    logging.debug("Parsed arguments")

    if not args.image:
        args.image = input("Enter the image path: ")

    if not args.text:
        args.text = input("Enter the caption text: ")

    return args

def manual_args(image: str, text: str, gif: bool = None, alpha: bool = None) -> Namespace:
    args = Namespace()
    args.image = image
    args.text = text
    args.gif = gif
    args.alpha = alpha
    return args
