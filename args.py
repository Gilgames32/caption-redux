import argparse

parser = argparse.ArgumentParser(description='Your script description here.')

parser.add_argument('-i', '--image', help='Image', default="")
parser.add_argument('-t', '--text', help='Text', default="")

args = parser.parse_args()


# manual
imgpath = args.image
while imgpath == "":
    imgpath = input("Enter image path: ").strip()

captiontext = args.text
while captiontext == "":
    captiontext = input("Enter caption: ")