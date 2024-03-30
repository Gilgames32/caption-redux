from src.pipeline import caption
from src import args

if __name__ == "__main__":
    args.correctparse()
    try:
        outpath = caption(args.imgpath, args.captiontext)
        print(f"\nFinished caption at {outpath}")
    except Exception as e:
        print(e)
