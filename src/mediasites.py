import re
import requests
import logging

def process_tenor(url):
    response = requests.get(url).text
    return response.split("contentUrl")[1].replace("\\u002F", "/").split("\"")[2]


def process_giphy(url):
    response = requests.get(url).text
    return "https://media" + response.split("https://media")[2].split("?")[0]


def process_imgflip(url):
    return url.replace("//", "//i.").replace("/gif", "") + ".gif"


url_processors = {
    r"https://tenor\.com/view": process_tenor,
    r"https://giphy\.com/gifs": process_giphy,
    r"https://imgflip\.com/gif/": process_imgflip,
}


def process_url(url):
    for pattern, processor in url_processors.items():
        if re.search(pattern, url):
            logging.info("Supported media link found")
            logging.debug(f"Corrected url to {url}")
            return processor(url)
    return url
