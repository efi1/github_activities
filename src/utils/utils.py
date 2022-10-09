import json
import os
import webbrowser
from pathlib import Path

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


def dict_to_obj(d):
    return json.loads(json.dumps(d), object_hook=obj)


def invoke_htm_file(file_name):
    if os.path.exists(file_name):
        url = F"file:{Path.joinpath(Path(__file__).parent.parent, file_name)}"
        webbrowser.open(url, new=2)  # open in new tab


def clear_htm_file(self, file_name='report.html'):
    os.rmdir(file_name)
