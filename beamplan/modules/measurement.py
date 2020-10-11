"""
Module containing the relevant measurement functionality for the beamplan package.

The following are functions that are to be used exclusively for the beamplan
package, and thus cannot be invoked via interpreter, but rather imported.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.User import User
from beamplan.classes.Sattelite import Sattelite
from beamplan.classes.Interference import Interference
from beamplan.classes.Entity import Entity
from beamplan import origin, userVisibleAngle, externalInterferenceAngle

from math import sqrt, acos, degrees, floor

def calculateAngle(v: Entity, a: Entity, b: Entity):
    """
    Calculates the angle formed between (point) a, the vertex, and (point) b

    Arguments:
        v (Entity) -- the vertex between the two points to get the angle between
        a (Entity) -- the first point provided
        b (Entity) -- the second point provided
    
    Returns:
        (float) -- angle between a and b (via the vertex)
    """

    # Calculate the point-differential (delta) between the points and the vertex
    deltaA = [a.getX() - v.getX(), a.getY() - v.getY(), a.getZ() - v.getZ()]
    deltaB = [b.getX() - v.getX(), b.getY() - v.getY(), b.getZ() - v.getZ()]

    # Calculate the magnitude of each
    magnitudeA = sqrt((deltaA[0] ** 2) + (deltaA[1] ** 2) + (deltaA[2] ** 2))
    magnitudeB = sqrt((deltaB[0] ** 2) + (deltaB[1] ** 2) + (deltaB[2] ** 2))

    # Calculate the norm of each vector
    normA = [deltaA[0] / magnitudeA, deltaA[1] / magnitudeA, deltaA[2] / magnitudeA]
    normB = [deltaB[0] / magnitudeB, deltaB[1] / magnitudeB, deltaB[2] / magnitudeB]

    # Calculate the dot product between the two
    dotProductAB = (normA[0] * normB[0]) + (normA[1] * normB[1]) + (normA[2] * normB[2])

    # Bound the dot product to prevent not being able to take acos (per evaluate.py)
    dotProductBoundAB = min(1.0, max(-1.0, dotProductAB))

    # Be verbose if the acos cannot be taken with the dot product
    if abs(dotProductBoundAB - dotProductAB) > 0.000001:
        print("# Notice: Dot product {} was bounded to {}".format(dotProductAB, dotProductBoundAB))
    
    return degrees(acos(dotProductBoundAB))

def satteliteIsVisible(user: User, sattelite: Sattelite):
    """
    Determines if the sattelite is visible to the user, given the constraints

    Arguments:
        user (User) -- user object for the user in question
        sattelite (Sattelite) -- sattelite object in question
    
    Returns:
        (boolean) -- True if the sattelite is visible to the user, False otherwise 
    """

    return calculateAngle(user, origin, sattelite) > 180.0 - userVisibleAngle

def isExternalInterference(user: User, interference: Interference, sattelite: Sattelite):
    """
    Determines if there is an external interference between the user and the sattelite,
    given a possible interference.

    Arguments:
        user (User) -- user object for the user in question
        interference (Interference) - interference object for the interference in question
        sattelite (Sattelite) - sattelite object for the sattelite in question
    
    Returns:
        (boolean) -- True if there is an interference, False if there is not
    """

    return not (calculateAngle(user, sattelite, interference) < externalInterferenceAngle)