"""
Class definition for the User child class (of Entity).

An User defined in the broadest sense is a Starlink user
on Earth.  Their coordinates are on the assumed round-earth.
All user norms pass through the center of the earth (0,0,0).
"""

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