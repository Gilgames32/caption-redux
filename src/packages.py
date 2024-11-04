import logging
import subprocess

def check_dependency(package):
    try:
        logging.debug(f"Checking for dependency: {package}")
        subprocess.run([package, '-h'], check=True, capture_output=True)
    except Exception:
        raise Exception(f'Missing dependency: {package}')