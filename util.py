import os
import random
import string
import re
from unidecode import unidecode

silence_tools = True
cwd = "./"
framenaming = "frame_%05d.png"


def ensure_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def clear_folder(path: str):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def generate_name(texto: str) -> str:
    # filenaming pattern, only letters, numbers and underscore
    fname = re.sub("[^\w_]", "_", unidecode(texto))
    # remove repeating underscores
    fname = re.sub("_{2,}", "_", fname)
    # trim and and random letters
    fname = fname[:16] + random_string(8)

    return fname
