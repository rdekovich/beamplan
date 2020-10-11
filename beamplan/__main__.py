#!/usr/bin/env python

"""
Main module called upon invocation to the beamplan package.

The beamplan package takes in a single text file containing
scenarios, providing sattelites, users and interferences - 
along with their respective locations.

The package parses the input, and determines how to best place
the beams to maximize the amount of users, with respect to the
constraints imposed on the system.  Some users might not be able
to be covered.

Provided positions use the ECEF coordinate system, described at
the source here: https://en.wikipedia.org/wiki/ECEF
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

import click
from os.path import abspath

from beamplan.modules.validate import validateInfile
from beamplan.modules.parse import parseInfile
from beamplan.modules.measurement import satteliteIsVisible, isExternalInterference

@click.command(help="A command-line tool to determine Starlink beam planning.")
@click.argument("infile")
@click.option("--debug", "-d", required=False, is_flag=True, help="Writes standard out to an *.out file")
def main(infile, debug):
    """
    Main module invoked upon package call.

    Takes required infile input to parse, processes input
    based on constraints of the problem, and outputs the results
    to standard out.  If debug is specified, it will also
    save the output to an equivalent *.out file.

    Arguments:
        infile {str} -- relative or full path of the input file to process
        debug {bool} -- flag that if true, will output to an *.out file as well
    
    Returns:
        Prints to standard out the output of the beamplan package call.
    """
    
    try:
        # Validate the infile from the user, raise descript error if invalid
        validateInfile(infile)
    except OSError as e:
        print("OSError: {}".format(e))
        exit()
    
    # Parse the input file into it's respective mappings and classes
    users, sattelites, interferences = parseInfile(abspath(infile))

    # For each of the users (Runtime: numUsers * max(numSattelites, numInterferences))
    for userID, user in users.items():
        # For each of the sattelites
        for _, sattelite in sattelites.items():
            # If this sattelite is visible to this user (constraint)
            if satteliteIsVisible(user, sattelite):
                # Add this user to the list of viable users for this sattelite
                sattelite.addViableUser(userID)
        
        # For each of the interferences
        for interferenceID, interference in interferences.items():
            # If this sattelite is visible to this user (constraint)
            if satteliteIsVisible(user, interference):
                # Add this interference to the list of possible interferences for the user
                user.addPossibleInterference(interferenceID)
    
    # For each sattelite (Runtime: numSattelites * numViableUsers[N] * numPossInterference[N])
    for _, sattelite in sattelites.items():
        # Acquire a copy of the viable users of the sattelite
        viableUsers = sattelite.getViableUsers().copy()

        # For each of the viable users for this sattelite
        for viableUserID in viableUsers:
            # Acquire the list of possible interferences for this user
            possibleInterferences = users[viableUserID].getPossibleInterferences()

            # For each possible interference
            for interferenceID, interference in interferences.items():
                # If there is an external interference between these..
