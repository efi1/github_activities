"""Minimal setup file for github assignment."""

from setuptools import find_packages, setup
# from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='github_activities',
    version='0.1.0',
    description='Manage various github activities',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # metadata
    author='Efi Ovadia',
    author_email='efovadia@gmail.com',
    license='proprietary',
    # install_requires=['pytest', 'GitPython']
    install_requires = [required, 'pytest-html', 'GitPython']
)
