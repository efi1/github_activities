"""Minimal setup file for github assignment."""

from setuptools import setup, find_packages

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
    install_requires=['pytest', 'GitPython', 'PyGithub', 'pytest-metadata']
)
