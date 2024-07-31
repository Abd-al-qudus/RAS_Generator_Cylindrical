#!/usr/bin/python3

"""this class contains the configuration of the 
    RAS Generator"""


class Configuration:
    """contains the RAS generator configuration"""
    def __init__(self, d, vf, vol_n, sd, r, h):
        if not isinstance(d, list):
            raise Exception('d must be a list containing the diameters')
        if len(d) == 0:
            raise Exception('diameters must not be empty')
        self.diameters = d
        self.vf= vf
        self.n = vol_n
        self.sd = sd
        self.n_min = 8
        self.n_max = 17
        self.r = r
        self.h = h
        self.vc = 3.142* self.h * self.r**2 
        self.d_min = min(self.diameters)
        self.d_max = max(self.diameters)
