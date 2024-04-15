import os
import random
import string
import re
import logging
from unidecode import unidecode
from emoji import demojize

silence_tools = True
silence_status = False
cwd = "./"
framenaming = "frame_%05d.png"


def ensure_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory {path}")


def clear_folder(path: str):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    logging.debug(f"Cleared {path}")


def random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def generate_name(texto: str) -> str:
    # filenaming pattern, only letters, numbers and underscore
    fname = re.sub("[^\w_]", "_", unidecode(demojize(texto)))
    # remove repeating underscores
    fname = re.sub("_{2,}", "_", fname)
    # trim and and random letters
    fname = fname[:16]
    if fname != "" and fname[-1] != "_":
        fname += "_"
    fname += random_string(8)

    logging.debug(f"Generated name {fname} from {texto if len(texto) < 16 else texto[:16] + '...'}")
    return fname
