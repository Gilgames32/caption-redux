import subprocess

def check_dependency(package):
    try:
        subprocess.run([package, '-h'], check=True, capture_output=True)
    except Exception:
        raise Exception(f'Missing dependency: {package}')