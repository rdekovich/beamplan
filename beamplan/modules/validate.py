"""
Module that contains validation checks for input(s) and intermediate data.

The following are functions that are to be used exclusively for the beamplan
package, and thus cannot be invoked via interpreter, but rather imported.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from os import path

def validateInfile(infile):
    """
    Validates the infile provided, throws errors if input is garbage.

    Arguments:
        infile {str} -- relative or full path of the input file to process
    
    Raises:
        OSError -- User provides input file/path that does not exist
        OSErrpr -- User provided a path that was not a file
    """

    # Validate existance of the path provided
    if path.exists(infile):
        # Validate that path provided is indeed a file
        if path.isfile(infile):
            return
        else:
            raise OSError("Input path provided is not a file.")
    else:
        raise OSError("Input file/path provided does not exist.")