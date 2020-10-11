"""
Class definition for the Entity parent class.

An Entity defined in the broadest sense is an object 
that exists ECEF coordinate-space.
"""

class Entity:
    """
    A parent object that exists within the ECEF coordinate space.

    This class possesses class functions to provide information about
    it, or relative to it when provided another instance of this class
    or a child.
    """

    def __init__(self, id, x, y, z, type):
        """
        Initializes the Entity class with it's X, Y and Z coordinates, along
        with it's unique ID.

        Arguments:
            id (int) -- the unique number ID of the entity
            x (float) -- the x coordinate of the entity (w.r.t the origin)
            y (float) -- the y coordinate of the entity (w.r.t the origin)
            z (float) -- the z coordinate of the entity (w.r.t the origin)
            type (string) -- the class of the entity (default is None)
        """

        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.type = type
    
    def getID(self):
        """
        Returns the stored ID of the Entity
        """
        return self.id
    
    def getType(self):
        """
        Returns the stored type of the Entity
        """
        return self.type