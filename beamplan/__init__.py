"""
Package root for the beamplan package and initialization.

This file, __init__.py, is required for package structuring
purposes.  This file makes Python treat directories containing
it as packages.  It can also be used for initializing for content
and special variables.

Source: https://docs.python.org/3/tutorial/modules.html#packages
"""

__author__ = "Robert Dekovich"
__email__ = "dekovich@umich.edu"
__status__ = "Development"

from beamplan.classes.Entity import Entity

"""The origin point of reference (center of the Earth)"""
origin = Entity(None, 0, 0, 0, None)

"""The number of beams allowed per sattelite (synonymous to # of connections)"""
beamsPerSattelite = 32

"""The number of colors of beams per sattelite"""
numColorsPerSattelite = 4

"""A list of the valid color IDs (e.g. A through D)"""
validColorIDs = [chr(ord('A') + i) for i in range(0, numColorsPerSattelite)]

"""
The maximum angle at which beams of the same color, on the same sattelite, must not
be less than (e.g. angle of 8 degrees is invalid)
"""
starlinkInterferenceAngle = 10.0

"""
The maximum angle at which Starlink beams must not be within of external interferers
(e.g. angle of 18 degrees between Starlink beam and external interference is invalid)
"""
externalInterferenceAngle = 20.0

"""
The maximum angle at which users can connect to a Starlink sattelite.  This angle
is with respect to degrees from the vertical (norm) of the user (e.g. +45 or -45)
"""
userVisibleAngle = 45.0