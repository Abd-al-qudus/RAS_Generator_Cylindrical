#!/usr/bin/python3

"""this class contains the configuration of the 
    RAS Generator"""


class Configuration:
    """contains the RAS generator configuration"""
    def __init__(self, d, vf, vol_n, sd, rad, h):
        if not isinstance(d, list):
            raise Exception('d must be a list containing the diameters')
        if len(d) == 0:
            raise Exception('diameters must not be empty')
        self.diameters = d
        # for keys in kwargs.keys():
        #     if not isinstance(kwargs.get(keys), (float, int)) or kwargs.get(keys) < 0:
        #         raise Exception('arguments must be an integer or float and greater than 0')
        self.vf= vf
        self.n = vol_n
        self.sd = sd
        # self.x_min = kwargs.get('x_min', None)
        # self.x_max = kwargs.get('x_max', None)
        # self.y_min = kwargs.get('y_min', None)
        # self.y_max = kwargs.get('y_max', None)
        # self.z_min = kwargs.get('z_min', None)
        # self.z_max = kwargs.get('z_max', None)
        self.rad = rad
        self.h = h
        self.vc = 3.142* self.h * self.rad**2 
        self.d_min = min(self.diameters)
        self.d_max = max(self.diameters)
