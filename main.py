from src.pipeline import caption
from src.args import imgpath, captiontext

if __name__ == "__main__":
    outpath = caption(imgpath, captiontext)
    print(f"\nFinished caption at {outpath}")
