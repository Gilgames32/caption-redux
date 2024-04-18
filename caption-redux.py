from src.pipeline import caption
from src import args
from src import config
import logging

if __name__ != "__main__":
    quit()

logging.basicConfig(level=config.loglevel)

args.correctparse()

try:
    outpath = caption(args.imgpath, args.captiontext)
    print(f"\nFinished caption at {outpath}")
except Exception as e:
    print(e)
