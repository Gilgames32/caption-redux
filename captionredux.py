import os
from .src import args, pipeline
from .src.config import Config


def caption(image: str, text: str, gif: bool = False, alpha: bool = False) -> str:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    arguments = args.manual_args(image, text, gif, alpha)
    config = Config(arguments)

    outpath = pipeline.caption(config)
    return outpath
