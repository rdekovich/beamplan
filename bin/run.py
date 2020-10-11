#!/usr/bin/env python

"""
Testing module to run all the tests against the package solution.

This module will clear all output files from the var/test folder,
re-run all the test input over the solution, and then run it against
the evaluate.py script in order to see coverage and constraint information.
"""

import subprocess
from os.path import isfile, abspath, join
from os import remove, listdir

"""The absolute location of the testing directory in the repository"""
TEST_ROOT = abspath("../var/tests/")

"""The output file extension"""
OUT_EXT = ".out"

"""The collective output file"""
OUTFILE = "output.txt"

def main():
    """
    Main module driver for run.py

    Will handle all I/O and running via Python subprocesses.
    """

    # Acquire all files in the testing directory
    files = [file for file in listdir(TEST_ROOT) if isfile(join(TEST_ROOT, file))]

    # Define a variable to hold the testing file path(s)
    testFiles = []

    # For each of the files
    for file in files:
        # If the file has the output extension on it
        if OUT_EXT in file:
            # Remove the file from the directory
            remove(join(TEST_ROOT, file))
        else:
            # Add the file to the list of test files
            testFiles.append(join(TEST_ROOT, file))

    # Create a new output file
    with open(join(TEST_ROOT, OUTFILE), "w") as outfile:
        outfile.write("Test output\n")
    
    # For each of the test files
    for infile in testFiles:
        # Run the package on the input
        subprocess.call(["beamplan", infile, "--debug"])

        # Evaluate the output
        subprocess.call(["python", "evaluate.py", infile, infile + '.out'])

if __name__ == "__main__":
    main()