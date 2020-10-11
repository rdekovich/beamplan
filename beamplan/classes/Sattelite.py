"""
Class definition for the Sattelite child class (of Entity).

A Sattelite defined in the broadest sense is a sattelite
that is an Entity, and is above Earth in orbit.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.Entity import Entity
from beamplan.classes.Beam import Beam

from beamplan import beamsPerSattelite, validColorIDs, starlinkInterferenceAngle
from beamplan.modules.measurement import calculateAngle

class Sattelite(Entity):
    """
    A child of Entity that signifies a sattelite in LEO.

    This class possesses additional data and methods, on top of the
    parent Entity.  A Starlink sattelite is capable of making up to
    32 independent beams simultaneously.  One sattelite can serve up
    to 32 concurrent users.

    Each beam is assigned one of 4 colors (A, B, C, D), which correspond
    to a particular frequency to serve the user.  This is necessary to allow
    a single sattelite to serve users that are close to one another without
    causing interference.
    """

    def __init__(self, id, x, y, z):
        """
        Initializes the Sattelite child class (Entity).

        Arguments:
            id (int) -- the unique number ID of the entity
            x (float) -- the x coordinate of the entity (w.r.t the origin)
            y (float) -- the y coordinate of the entity (w.r.t the origin)
            z (float) -- the z coordinate of the entity (w.r.t the origin)
        """
        
        super().__init__(id, x, y, z, "sattelite")

        # Define a list of viable users this sattelite can satisfy with
        self.viableUsers = []

        # Define a list of beams this sattelite is making
        self.beams = []
    
    def addViableUser(self, userID):
        """
        Add a viable user to the list of viable users
        """
        self.viableUsers.append(userID)
    
    def removeViableUser(self, userID):
        """
        Remove a viable user from the list of viable users
        """
        self.viableUsers.remove(userID)
    
    def getViableUsers(self):
        """
        Returns the list of viable users
        """
        return self.viableUsers
    
    def getBeams(self):
        """
        Returns the list of Beams made by this sattelite.
        """
        return self.beams
    
    def addBeam(self, userID, color):
        """
        Adds a single beam to the list of beams this sattelite has made

        Arguments:
            userID {int} -- ID of the user to add to the beam
            color {string} -- string representation of the color to be added
        """
        self.beams.append(Beam(len(self.beams) + 1, self.id, userID, color))
    
    def beamFactory(self, existingBeams, getUser):
        """
        Creates as many possible beams given constraints, and existing connections.

        Arguments:
            existingBeams {dict} -- mapping of beamID to sattelite ID for bookkeeping
            getUser (func) -- function to retrieve the User object of a given ID
        
        Returns:
            {dict} -- updated dictionary of beams added
        """

        # For each of the remaining viable users
        for userID in self.viableUsers:
            # If there is no more room on this sattelite
            if len(self.beams) == beamsPerSattelite:
                break

            # If this user has been served already (by another sattelite)
            if userID in existingBeams:
                # Move onto the next one
                continue

            # Iterate through each potential color of beam (starting with A)
            for color in validColorIDs:
                # Create a subset of matching colors
                matching = [beam for beam in self.beams if beam.getColor() == color]

                # If the list is empty, make the beam
                if not matching:
                    self.addBeam(userID, color)
                    existingBeams[userID] = self.id
                    break
                else:
                    # Define a tracker variable to determine an invariant was broken
                    beamPossible = True

                    # For each of the beams that match in color
                    for beam in matching:
                        # Get the User object(s) from the callback function
                        userA = getUser(userID)
                        userB = getUser(beam.getUserID())

                        # Calculate the angle between userA and userB given the sattelite
                        angle = calculateAngle(Entity(None, self.x, self.y, self.z, None), userA, userB)

                        # If the angle is less than the maximum
                        if angle < starlinkInterferenceAngle:
                            # Cannot add the beam, invariant broken
                            beamPossible = False
                            break
                    
                    # If the beam is possible after constraint checking
                    if beamPossible:
                        # Add the beam
                        self.addBeam(userID, color)
                        existingBeams[userID] = self.id
                        break
        
        return existingBeams