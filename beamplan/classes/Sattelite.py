"""
Class definition for the Sattelite child class (of Entity).

A Sattelite defined in the broadest sense is a sattelite
that is an Entity, and is above Earth in orbit.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.Entity import Entity

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
    
    def __str__(self):
        """
        Overload of the special variable __str__.

        Will print out what is returned when a Sattelite is printed (e.g. print(Sattelite))
        """
        return "viable users: {}".format(self.viableUsers)
    
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