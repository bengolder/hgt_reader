'''This module provides a simple script for converting hgt coordinates into
Rhino points. Keep in mind that the 'points' in an hgt file are based on
longitude and latitude, in the EPSG 436 geographic projection. This means that
at some places on the earth, the longitude (or 'y') coordinates are about 90
meters apart, while they are closer together in areas closer to the poles. The
height values are measured in meters about sea level, and therefore if these
coordinates are not reprojected, they greatly exaggerate the height of any
area, by a factor up to about 90.
'''

import Rhino
import scriptcontext

def to_point(xyz_tuple):
    return Rhino.Geometry.Point3d(*xyz_tuple)

def grid_to_points(hgt_read_results):
    for row in hgt_read_results:
        for coord in row:
            yield to_point(coord)

def grid_to_doc(hgt_read_results):
    for row in hgt_read_results:
        for coord in row:
            scriptcontext.doc.Objects.AddPoint(*coord)
    print 'complete'

def grid_to_point_cloud(hgt_read_results):
    pt_cloud = Rhino.Geometry.PointCloud()
    for row in hgt_read_results:
        for coord in row:
            pt_cloud.Add(to_point(coord))
    return pt_cloud

def bake_point_cloud(hgt_read_results):
    pc = grid_to_point_cloud(hgt_read_results)
    scriptcontext.doc.Objects.AddPointCloud(pc)
    print 'complete'



