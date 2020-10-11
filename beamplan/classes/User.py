"""
Class definition for the User child class (of Entity).

An User defined in the broadest sense is a Starlink user
on Earth.  Their coordinates are on the assumed round-earth.
All user norms pass through the center of the earth (0,0,0).
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.Entity import Entity

class User(Entity):
    """
    A child of Entity that signifies an Earth user of Starlink.

    This class possesses additional data and methods, on top of the parent
    Entity, that are solely unique to an Earth-bound user
    """

    def __init__(self, id, x, y, z):
        """
        Initializes the User child class (Entity).

        Arguments:
            id (int) -- the unique number ID of the entity
            x (float) -- the x coordinate of the entity (w.r.t the origin)
            y (float) -- the y coordinate of the entity (w.r.t the origin)
            z (float) -- the z coordinate of the entity (w.r.t the origin)
        """
        
        super().__init__(id, x, y, z, "user")

        # Define a list of possible interferences that this user may run into
        self.possibleInterferences = []
    
    def __str__(self):
        return "possible interferences: {}".format(self.possibleInterferences)
    
    def addPossibleInterference(self, interferenceID):
        """
        Adds a possible interference that the user may encounter
        """
        self.possibleInterferences.append(interferenceID)
    
    def removePossibleInterference(self, interferenceID):
        """
        Removes a possible interference that the user will not encounter anymore
        """
        self.possibleInterferences.remove(interferenceID)