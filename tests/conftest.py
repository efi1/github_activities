"""Shared fixtures."""
import os  # being used in func: pytest_addoption
from pathlib import Path # being used in func: pytest_addoption


from pytest import fixture
from github import Github, Auth
from tests import settings
from utils.utils import dict_to_obj
from src.clients.tests_client import TestsClient


settings_items = [i for i in settings.__dir__() if not i.startswith('_')]


def pytest_addoption(parser) -> None:
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
    return Github(auth=(Auth.Token(tests_data.token)))


@fixture(scope="function")
def tests_client(github_client, tests_data):
    tests_client = TestsClient(github_client, tests_data)
    tests_client.tear_down()
    yield tests_client

