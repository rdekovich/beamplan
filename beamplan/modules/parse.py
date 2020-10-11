"""
Module the contains parsing functionality for the input file and beyond.

The following are functions that are to be used exclusively for the beamplan
package, and thus cannot be invoked via interpreter, but rather imported.
"""

from beamplan.classes.Entity import Entity
from beamplan.classes.User import User
from beamplan.classes.Sattelite import Sattelite
from beamplan.classes.Interference import Interference

def parseLineIntoClass(line, num, type):
    """
    Parses a line of input into a respective class object, returns the class object.

    Arguments:
        line {string} -- line of the input file to parse into information
        num {int} -- line number of the line provided (debugging purposes)
        type {"user", "sattelite", "interference"} -- type of class to load into
    
    Raises:
        ValueError -- bad ID provided (cannot convert)
        ValueError -- bad x-coordinate, y-coordinate or z-coordinate (cannot convert)
    
    Returns:
        {User, Sattelite, Interference} - child class of Entity of the object parsed
    """
    id = None
    x = None
    y = None
    z = None
    outputClass = None

    # Split the line by whitespace
    info = line.split()

    try:
        # Acquire the ID provided in the input line
        id = int(info[1])
    except ValueError:
        raise ValueError("ID provided for line {} could not be converted to int.".format(num))

    try:
        # Acquire the x-coordinate (float) in the input line
        x = float(info[2])
    except ValueError:
        raise ValueError("X-coordinate provided for line {} could not be converted to float.".format(num))

    try:
        # Acquire the y-coordinate (float) in the input line
        y = float(info[3])
    except ValueError:
        raise ValueError("Y-coordinate provided for line {} could not be converted to float.".format(num))

    try:
        # Acquire the z-coordinate (float) in the input line
        z = float(info[4])
    except ValueError:
        raise ValueError("Z-coordinate provided for line {} could not be converted to float.".format(num))
    
    # Create the proper output class for the line
    if type == "user":
        outputClass = User(id, x, y, z)
    elif type == "sattelite":
        outputClass = Sattelite(id, x, y, z)
    elif type == "interference":
        outputClass = Interference(id, x, y, z)
    else:
        # Valid, but should NEVER happen!
        outputClass = Entity(id, x, y, z, None)
    
    return outputClass


def parseInfile(infile):
    """
    Parses the input file into it's respective divisions and classes, returns mapping.

    The function will skip over comments, and asses which class certain input falls into
    for the beamplan package classes.  A user is to provide input of either one of the
    following:

    User: 
        An Earth-bound entity that is trying to connect to Starlink
    Sattelite: 
        A Starlink sattelite attempting to reciprocate requests via beams
    Interference:
        An external sattelite to be avoided in constraining the beams for Starlink

    Arguments:
        infile {string} -- absolute path of the input file to be parsed
    
    Returns:
        TODO
    """
    users = {}
    sattelites = {}
    interferences = {}

    try:
        with open(infile, 'r') as f:
            # For each line in the file
            for num, line in enumerate(f.readlines()):
                # If the line was a comment, pass over (skip)
                if '#' in line:
                    continue
                elif line.strip() == '':
                    continue
                elif "user" in line:
                    # Parse the line, populate a User class
                    user = parseLineIntoClass(line, num, "user")

                    # Add it to the user mapping
                    users[user.getID()] = user
                elif "sat" in line:
                    # Parse the line, populate a Sattelite class
                    sattelite = parseLineIntoClass(line, num, "sattelite")

                    # Add it to the sattelite mapping
                    sattelites[sattelite.getID()] = sattelite
                elif "interferer" in line:
                    # Parse the line, populate an Interference class
                    interference = parseLineIntoClass(line, num, "interference")

                    # Add it to the interference mapping
                    interferences[interference.getID()] = interference
                else:
                    continue
        
    except ValueError as e:
        print(e)
        exit()

    return users, sattelites, interferences