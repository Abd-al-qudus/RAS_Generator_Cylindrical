#!/usr/bin/python3

"""This class contains all the check cases.
    the sole checks are based on the boundary check 
    and the radial check. The geometric intersection
    check is not used in this case"""

from math import sqrt


class Checker:
    """contains the checks on each polygons"""

    def __init__(self, ellipsoid, rad, h, ellipsoids, sd):
        """initialize the checker class"""
        self.ellipsoid = ellipsoid
        self.r = rad
        self.h = h
        self.ellipsoids = ellipsoids
        self.sd = sd

    def init_check_ellipsoid_in_bound(self):
        """
            checker for the boundary conditions of the polyhedron,
            considering wall effect, each polyhedron at the 
            boundary is at a distance of size distribution * 
                diameter of the polyhedron
        """
        xy = ((self.r - self.ellipsoid[6])**2 + (self.r - self.ellipsoid[7])**2)**0.5
        if xy + self.ellipsoid[1] > self.r - 0.1:
            return False
        if self.ellipsoid[6] - self.ellipsoid[0] < 0.1 or self.ellipsoid[6] + self.ellipsoid[0] > 2 * self.r - 0.1:
            return False
        if self.ellipsoid[8] - self.ellipsoid[0] < 0.1 or self.ellipsoid[8] + self.ellipsoid[0] > self.h - 0.1:
            return False
        return True

    def init_is_radially_separated(self):
        """check the radial separation of the two sphere"""
        for center in self.ellipsoids:
            dist = sqrt(((center[6] - self.ellipsoid[6])**2) + ((center[7] - self.ellipsoid[7])**2) + ((center[8] - self.ellipsoid[8])**2))
            if dist <= 1.05 * (center[0] + self.ellipsoid[0]):
                return False
        return True

    def init_all_checks(self):
        """check whether the polyhedron is not overriding others"""
        radial = self.init_is_radially_separated()
        bound = self.init_check_ellipsoid_in_bound()
        return bound and radial
