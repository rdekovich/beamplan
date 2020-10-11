"""
Class definition for the Beam class.

A Beam is defined as a "made" connection between
a sattelite and a user.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

class Beam:
    """
    A class representing the data associated with a Beam object.

    A Beam is a connection made between a Sattelite and a User.  It
    has metadata associated with it's connection to link it back to
    what it is connected to.
    """

    def __init__(self, beamID, satteliteID, userID, color):
        """
        Initializes a Beam class to with a set of parameters.

        Args:
            beamID {str} -- the ID (number) of the beam on the Sattelite
            satteliteID {int} -- the ID (number) of the Sattelite connection
            userID {int} -- the ID (number) of the User being connected to
            color {str} -- the color of the beam
        """
        self.beamID = beamID
        self.satteliteID = satteliteID
        self.userID = userID
        self.color = color
    
    def __str__(self):
        """
        Overload of the special variable __str__.

        When print(Beam) is called, it will print the return value of this.
        """
        return "sat {} beam {} user {} color {}".format(self.satteliteID, self.beamID, self.userID, self.color)
    
    def getColor(self):
        """
        Returns the color of the beam.
        """
        return self.color
    
    def getUserID(self):
        """
        Returns the userID of the beam.
        """
        return self.userID