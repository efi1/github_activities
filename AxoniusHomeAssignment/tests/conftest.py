"""Shared fixtures."""
import os  # being used in func: pytest_addoption
import logging
import webbrowser
from pathlib import Path
from pytest import fixture
from github import Github
from tests import settings
from utils.utils import dict_to_obj, invoke_htm_file
from src.clients.tests_client import TestsClient

# logging.getLogger()

settings_items = [i for i in settings.__dir__() if not i.startswith('_')]


def pytest_addoption(parser):
    for item in settings_items:
        try:
            value = eval(getattr(settings, item))
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            value = getattr(settings, item)
        parser.addoption(F"--{item}", action='store', default=value)


@fixture(scope="session")
def tests_data(request):
    data = dict()
    for item in settings_items:
        data[item] = request.config.getoption(F"--{item}")
    return dict_to_obj(data)


@fixture(scope="session")
def github_client(tests_data):
    return Github(login_or_token=tests_data.token)


@fixture(scope="function")
def tests_client(github_client, tests_data):
    tests_client = TestsClient(github_client, tests_data)
    tests_client.tear_down()
    yield tests_client
    # _invoke_htm_file('report.htm')


def _invoke_htm_file(file_name):
    # if os.path.exists(file_name):
    # request.config.getoption(F"--html"):
    url = F"file:{Path.joinpath(Path(__file__).parent.parent, file_name)}"
    webbrowser.open(url, new=2)


# @pytest.fixture(scope="session")
# def my_setup(request):
#     print('\nDoing setup')
#     def fin():
#         url = F"file:{Path.joinpath(Path(__file__).parent.parent, 'report.html')}"
#         webbrowser.open(url, new=2)
#     request.addfinalizer(fin)
