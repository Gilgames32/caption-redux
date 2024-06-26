from src.pipeline import caption
from src import args
import logging

if __name__ != "__main__":
    quit()

logging.basicConfig(level=logging.INFO)
logging.getLogger("PIL").setLevel(logging.WARNING)

args.correctparse()

try:
    outpath = caption(args.imgpath, args.captiontext)
    print(f"\nFinished caption at {outpath}")
except Exception as e:
    print(e)
