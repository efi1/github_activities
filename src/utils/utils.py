import json
import os
import webbrowser
from pathlib import Path


class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


class HtmlReport(object):
    def __init__(self, tests_data):
        self.url_path = F"file:{Path.joinpath(Path(__file__).parent.parent, tests_data.results_target, tests_data.html_report_name)}"

    def invoke_htm_file(self):
        if os.path.exists(self.url_path):
            # url = F"file:{Path.joinpath(Path(__file__).parent.parent, file_name)}"
            webbrowser.open(self.url_path, new=2)  # open in new tab

    def clear_htm_file(self, file_name='report.html'):
        os.rmdir(self.url_path)


def dict_to_obj(d):
    return json.loads(json.dumps(d), object_pairs_hook=obj)
