"""
Class definition for the Sattelite child class (of Entity).

An Interference defined in the broadest sense is a sattelite
that is an Entity, and is a interference to the constraint
problem of the Starlink sattelites.
"""

from beamplan.classes.Entity import Entity

class Interference(Entity):
    """
    A child of Entity that signifies an interfering constraint in LEO.

    This class possesses additional data and methods, on top of the
    parent Entity.  An interference sattelite is an entity that must
    be avoided in terms of beams and beam-density.  The beams of
    Starlink sattelites must not be within 20 degrees of any of these.
    """

    def __init__(self, id, x, y, z):
        """
        Initializes the Interference child class (Entity).

        Arguments:
            id (int) -- the unique number ID of the entity
            x (float) -- the x coordinate of the entity (w.r.t the origin)
            y (float) -- the y coordinate of the entity (w.r.t the origin)
            z (float) -- the z coordinate of the entity (w.r.t the origin)
        """
        
        super().__init__(id, x, y, z, "interference")