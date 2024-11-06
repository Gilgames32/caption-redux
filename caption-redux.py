import os
import logging
from src import args, pipeline
from src.config import Config

def caption(image: str, text: str, gif: bool = False, alpha: bool = False) -> str:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    arguments = args.manual_args(image, text, gif, alpha)
    config = Config(arguments)

    outpath = pipeline.caption(config)
    return outpath

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    arguments = args.parse_args()
    config = Config(arguments)
    logging.getLogger().setLevel(getattr(logging, config.loglevel))

    try:
        outpath = pipeline.caption(config)
        print(f"\nFinished caption at {outpath}")
    except Exception as e:
        print(f"\nFailed to create caption")
        print(e)

if __name__ == "__main__":
    main()