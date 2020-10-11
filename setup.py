#!/usr/bin/env python

"""
Setup package installation file for the beamplan package.

The module is best invoked in a sourced virtual environment,
that way, all your scripts and site-package folders will be
within the project directory.  The invocation is as follows:

$ pip install -e .
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from setuptools import setup

setup(
    name="beamplan",
    version="0.0.0",
    description="A command-line tool to determine Starlink beam planning.",
    author=__author__,
    author_email=__email__,
    packages=["beamplan"],
    include_package_data=True,
    install_requires=[
        "pycodestyle==2.5.0",
        "click==7.1.2"
    ],
    entry_points={
        "console_scripts": [
            "beamplan = beamplan.__main__:main"
        ]
    }
)