"""
Class definition for the Satellite child class (of Entity).

A Satellite defined in the broadest sense is a satellite
that is an Entity, and is above Earth in orbit.
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.Entity import Entity
from beamplan.classes.Beam import Beam

from beamplan import beamsPerSatellite, validColorIDs, starlinkInterferenceAngle, numColorsPerSatellite
from beamplan.modules.measurement import calculateAngle

import random

class Satellite(Entity):
    """
    A child of Entity that signifies a satellite in LEO.

    This class possesses additional data and methods, on top of the
    parent Entity.  A Starlink satellite is capable of making up to
    32 independent beams simultaneously.  One satellite can serve up
    to 32 concurrent users.

    Each beam is assigned one of 4 colors (A, B, C, D), which correspond
    to a particular frequency to serve the user.  This is necessary to allow
    a single satellite to serve users that are close to one another without
    causing interference.
    """

    def __init__(self, id, x, y, z):
        """
        Initializes the Satellite child class (Entity).

        Arguments:
            id (int) -- the unique number ID of the entity
            x (float) -- the x coordinate of the entity (w.r.t the origin)
            y (float) -- the y coordinate of the entity (w.r.t the origin)
            z (float) -- the z coordinate of the entity (w.r.t the origin)
        """
        
        super().__init__(id, x, y, z, "satellite")

        # Define a list of viable users this satellite can satisfy with
        self.viableUsers = []

        # Define a list of beams this satellite is making
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
        Returns the list of Beams made by this satellite.
        """
        return self.beams
    
    def addBeam(self, userID, color):
        """
        Adds a single beam to the list of beams this satellite has made

        Arguments:
            userID {int} -- ID of the user to add to the beam
            color {string} -- string representation of the color to be added
        """
        self.beams.append(Beam(len(self.beams) + 1, self.id, userID, color))
    
    def beamFactory(self, existingBeams, getUser):
        """
        Creates as many possible beams given constraints, and existing connections.

        Arguments:
            existingBeams {dict} -- mapping of beamID to satellite ID for bookkeeping
            getUser (func) -- function to retrieve the User object of a given ID
        
        Returns:
            {dict} -- updated dictionary of beams added
        """

        # If there exists viable users for this satellite
        if self.viableUsers:
            # Find the maximum assignments of users to beams
            assignments = self.recursiveDFS([], 0, getUser, existingBeams)

            # For each assignment
            for assignment in assignments:
                # Create and add the beam to the list
                self.addBeam(assignment[0], assignment[1])

                # Add it to the existing mapping
                existingBeams[assignment[0]] = self.id
        
        return existingBeams
    
    def recursiveDFS(self, assignments, userIndex, getUser, existing):
        """
        Recursive DFS with no pruning, looks at all possible combinations
        of assignments for beams to viable users, and finds the assignment
        that provides the most users covered.

        This metric is not all that useful, as it takes forever to run.
        """

        # If there is no more users to choose from
        if userIndex == len(self.viableUsers):
            # Return current assignment of users to colors
            return assignments
    
        # If there is no more room on the satellite
        if len(assignments) == beamsPerSatellite:
            # Return current assignment of users to colors
            return assignments
        
        # If the user already is mapped to
        if self.viableUsers[userIndex] in existing:
            # Skip this assignment, move to the next user
            return self.recursiveDFS(assignments, userIndex + 1, getUser, existing)

        # Create an array to hold maximum found
        maximumAssignment = []

        # Acquire the user object for the given User
        userA = getUser(self.viableUsers[userIndex])

        # For each of the colors the satellite can handle
        for color in validColorIDs:
            # Find a list of all the assignments that have this color
            matching = [beam for beam in assignments if beam[1] == color]

            # Create a copy of the assignments array
            assignCopy = assignments.copy()

            # If there is no matching colors
            if not matching:
                # Add this userID -> color pair to the assignments
                assignCopy.append([self.viableUsers[userIndex], color])

                # Try to add this color to the sequence assignment, find it's max
                attemptedAssignment = self.recursiveDFS(assignCopy, userIndex + 1, getUser, existing)

                # If the length of the attempted one is greater than the current
                if len(attemptedAssignment) > len(maximumAssignment):
                    # Set the attempted to the new maximum
                    maximumAssignment = attemptedAssignment
            else:
                # Define a tracker variable to see if the beam is possible
                beamPossible = True

                # For each of the matching assignments
                for match in matching:
                    # Acquire the users information
                    userB = getUser(match[0])

                    # Calculate the angle in between A and B with respect to the satellite
                    angle = calculateAngle(Entity(None, self.x, self.y, self.z, None), userA, userB)

                    # If the angle is less than the maximum (doesn't meet constraint)
                    if angle < starlinkInterferenceAngle:
                        beamPossible = False
                        break
                
                # If the beam is possible
                if beamPossible:
                    # Add this userID -> color pair to the assignments
                    assignCopy.append([self.viableUsers[userIndex], color])

                    # Try to add this color to the sequence assignment, find it's max
                    attemptedAssignment = self.recursiveDFS(assignCopy, userIndex + 1, getUser, existing)

                    # If the length of the attempted one is greater than the current
                    if len(attemptedAssignment) > len(maximumAssignment):
                        # Set the attempted to the new maximum
                        maximumAssignment = attemptedAssignment
                else:
                    # Attempt this assignment without adding a color
                    attemptedAssignment = self.recursiveDFS(assignCopy, userIndex + 1, getUser, existing)

                    # If the length of the attempted one is greater than the current
                    if len(attemptedAssignment) > len(maximumAssignment):
                        # Set the attempted to the new maximum
                        maximumAssignment = attemptedAssignment
        
        return maximumAssignment