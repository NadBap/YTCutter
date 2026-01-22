import json
import os
import sys
import tempfile

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def atomic_write_json(path, data):
    """Safely write JSON to disk using atomic replace."""
    dir_name = os.path.dirname(path)

    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False) as tmp:
        json.dump(data, tmp, indent=4)
        tmp_path = tmp.name

    os.replace(tmp_path, path)