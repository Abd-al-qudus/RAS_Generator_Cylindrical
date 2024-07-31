#!/usr/bin/python3

"""this class contains the RAS Generator logics"""
import math
import random
from scipy.spatial import ConvexHull
from configurations import Configuration
from storage import Storage
from checker import Checker


class Generator:
    """generates the RAS coordinates"""
    def __init__(self, config, storage):
        if not isinstance(config, Configuration):
            raise Exception('config must be a configuration class')
        self.config = config
        if not isinstance(storage, Storage):
            raise Exception('storage must be a storage class')
        self.storage = storage
        self.check = Checker

    def compute_volume(self, d, vf, vc, n, d_min, d_max):
        """compute the volume per segment for generation of aggregates"""
        volume = []
        p_mnd = 100 * ((d_min / d_max) ** n)
        p_mxd = 100 * ((d_max / d_max) ** n)
        for i in range(len(d)):
            if i + 1 != len(d):
                p_d = 100 * ((d[i] / d_max) ** n)
                p_nd = 100 * ((d[i + 1] / d_max) ** n)
                bound_vol = ((p_nd - p_d) / (p_mxd - p_mnd)) * vf * vc
                vol_obj = {
                            'volume': bound_vol,
                            'diameters': [d[i], d[i + 1]]
                        }
                volume.append(vol_obj)
        volume = sorted(volume, key=lambda k: k['diameters'])
        volume = volume[-1::-1]
        return volume
    
    def compute_hd_vbound(self, p, d, vf, vc):
        """compute hard-coded volume fraction"""
        volume = []
        p_max = max(p)
        p_min = min(p)
        for i in range(len(d)):
            if i + 1 != len(d):
                p_d = p[i]
                p_dn = p[i + 1]
                bound_vol = ((p_dn - p_d) / (p_max - p_min)) * vf * vc
                vol_obj = {
                            'volume': bound_vol,
                            'diameters': [d[i], d[i + 1]]
                        }
                volume.append(vol_obj)
        volume = sorted(volume, key=lambda k: k['diameters'])
        volume = volume[-1::-1]
        return volume
    
    def generate_polyhedron(self, d, rad, h, n_min, n_max):
        """generate polyhedrons faces"""
        poly_coordinates = []
        r = (min(d) / 2) + random.uniform(0, 1) * ((max(d)/ 2) - (min(d) / 2))
        n = n_min + random.uniform(0, 1) * (n_max - n_min)
        x_o = random.uniform(0, 1) * 2 * rad
        y_o = random.uniform(0, 1) * 2 * rad
        z_o = random.uniform(0, 1) * h
        for i in range(round(n)):
            polar_corr = random.uniform(0, 1)
            azimuth_corr = random.uniform(0, 1)
            azimuth_angle = azimuth_corr * math.pi
            polar_angle = polar_corr * math.pi * 2
            x_i = r * math.cos(polar_angle) * math.sin(azimuth_angle) + x_o
            y_i = r * math.cos(azimuth_angle) * math.sin(polar_angle) + y_o
            z_i = r * math.cos(azimuth_angle) + z_o
            poly_coordinates.append([x_i, y_i, z_i])
        return poly_coordinates, [x_o, y_o, z_o, r]

    def wrapper(self):
        """initialize the operation"""

        # mini vertex distance checker
        def vertex_space(poly, r):
            """check if the distance between the vertexes >= 0.5r"""
            for i in range(0, len(poly)):
                for j in range(i + 1, len(poly)):
                    dist = math.sqrt(((poly[i][0] - poly[j][0])**2) + ((poly[i][0] - poly[j][0])**2) + ((poly[i][0] - poly[j][0])**2))
                    if dist < 0 * r:
                        return False
                    
            return True
        

        vc = 0
        vr = 0
        vl = 0
        volumes = self.compute_volume(
            self.config.diameters,
            self.config.vf,
            self.config.vc,
            self.config.n,
            self.config.d_min,
            self.config.d_max
        )
        # volumes = self.compute_hd_vbound(
        #     self.config.p,
        #     self.config.diameters,
        #     self.config.vf,
        #     self.config.vc
        # )
        print(volumes)
        for v in volumes:
            print(v['diameters'])
            if vr > 0:
                v['volume'] += vr
                vr = 0
            while vc <= v['volume']:
                result, center = self.generate_polyhedron(
                    v['diameters'],
                    self.config.r,
                    self.config.h,
                    self.config.n_min,
                    self.config.n_max)
                # if vertex_space(result, center[-1]):
                #     continue

                # p_vol = 4/3 * (math.pi * (center[-1] ** 3))
                # p_vol = ConvexHull(result).volume
                # if center[-1] < 7.5:
                #     p_vol = ConvexHull(result).volume * 2.0
                p_vol = (4 * (math.pi) * (center[-1] ** 3)) / 3
                if len(self.storage.polyhedrons) > 0:
                    if self.check(result, 
                        self.storage.polyhedrons, 
                        self.config.r,
                        self.config.h, 
                        center, 
                        self.storage.centers,
                        self.config.sd).init_all_checks():
                        # co_vol += (4/3 * (math.pi * center[-1] ** 3)) - ConvexHull(result).volume
                        self.storage.store_polyhedrons(result)
                        self.storage.store_centers(center)
                        vc += p_vol
                        vl = p_vol
                        print(len(self.storage.polyhedrons), v['volume'], vc)
                        # print('----------------------------------------')
                        # print(self.storage.polyhedrons)
                        # print(result)
                    else:
                        continue
                else:
                    # print(center)
                    if self.check(result, 
                        self.storage.polyhedrons, 
                        self.config.r,
                        self.config.h, 
                        center, 
                        self.storage.centers,
                        self.config.sd).init_check_polygon_in_bound():
                        self.storage.store_polyhedrons(result)
                        self.storage.store_centers(center)
            if v['volume'] - vc + vl > 0:
                vr += v['volume'] - vc + vl
            del self.storage.polyhedrons[-1]
            del self.storage.centers[-1]
            print(v['volume'], vc, vl, vr)
            vc = 0
        # print('co----: ', co_vol)

