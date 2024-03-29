import pipeline
from args import imgpath, captiontext

if __name__ == '__main__':
    outpath = pipeline.caption(imgpath, captiontext)
    print(f"\nFinished caption at {outpath}")
