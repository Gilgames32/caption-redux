import os

devmode = True
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