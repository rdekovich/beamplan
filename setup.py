#!/usr/bin/env python3.9

"""
Setup package installation file for the beamplan package.

Module can be invoked in two ways.  First, it can be
called by invoking the interpreter directly.  This is
done by the following:

$ ./setup.py

It can also be invoked via pip.  This can be done by the
following:

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