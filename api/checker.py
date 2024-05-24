#!/usr/bin/python3

"""This class contains all the check cases.
    the sole checks are based on the boundary check 
    and the radial check. The geometric intersection
    check is not used in this case"""

import numpy as np
from scipy.spatial import ConvexHull
from math import sqrt


class Checker:
    """contains the checks on each polygons"""

    def __init__(self, coordinates, bounds, centers, sd):
        """initialize the checker class"""
        self.coordinates = coordinates
        self.bounds = bounds
        self.centers = centers
        self.sd = sd

    def init_check_sphere_in_bound(self, coordinates, bounds):
        """
            checker for the boundary conditions of the polyhedron,
            considering wall effect, each polyhedron at the 
            boundary is at a distance of size distribution * 
                diameter of the polyhedron
        """
        x_min, x_max, y_min, y_max, z_min, z_max = bounds
        if coordinates[0] + coordinates[3] < x_min + (self.sd * self.coordinates[3] * 2) or coordinates[0] + coordinates[3] > x_max - (self.sd * self.coordinates[3] * 2):
            return False
        if coordinates[1] + coordinates[3] < y_min + (self.sd * self.coordinates[3] * 2) or coordinates[1] + coordinates[3] > y_max - (self.sd * self.coordinates[3] * 2):
            return False
        if coordinates[2] + coordinates[3] < z_min + (self.sd * self.coordinates[3] * 2) or coordinates[2] + coordinates[3] > z_max - (self.sd * self.coordinates[3] * 2):
            return False
        return True

    def init_is_radially_separated(self, coordinates, centers):
        """check the radial separation of the two sphere"""
        for center in centers:
            dist = sqrt(((center[0] - coordinates[0])**2) + ((center[1] - coordinates[1])**2) + ((center[2] - coordinates[2])**2))
            if dist <= center[3] + coordinates[3]:
                return False
        return True

    def init_all_checks(self):
        """check whether the polyhedron is not overriding others"""
        radial = self.init_is_radially_separated(self.coordinates, self.centers)
        bound = self.init_check_sphere_in_bound(self.coordinates, self.bounds)
        return bound and radial
