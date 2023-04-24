from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from QPoint3DF import *
from edge import *
from triangle import *

class Algorithms:
    def __init__(self):
        pass

    def get2LinesAngle(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF, p4: QPoint3DF):
        # compute vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # dot product
        uv = (ux * vx) + (uy * vy)

        # norms
        nu = sqrt(ux**2 + uy**2)
        nv = sqrt(vx**2 + vy**2)

        arg = uv / (nu * nv)
        arg = max(min(arg, 1), -1)

        # angle
        return acos(arg)

    def getPointLinePosition(self, p: QPoint3DF, p1: QPoint3DF, p2: QPoint3DF):
        # compute vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p.x() - p1.x()
        vy = p.y() - p1.y()

        # compute determinant
        t = ux * vy - uy * vx

        # point is in the left halfplane
        if t > 0:
            return 1

        # point is in the right halfplane
        if t < 0:
            return 0

        # colinear point
        return -1

    # find optimal Delaunay point
    def getDelaunayPoint(self, p1: QPoint3DF, p2: QPoint3DF, points: list[QPoint3DF]):
        idx_max = -1
        om_max = 0

        # process all points
        for i in range(len(points)):
            # exclude identical points
            if (points[i] != p1) and (points[i] != p2):
                # point in the left halfplane
                if self.getPointLinePosition(points[i], p1, p2) == 1:
                    # compute angle
                    om = self.get2LinesAngle(points[i], p1, points[i], p2)

                    # update maximum
                    if om > om_max:
                        om_max = om
                        idx_max = i

        return idx_max

    # find nearest point
    def getNearestPoint(self, p: QPoint3DF, points: list[QPoint3DF]):
        idx_min = -1
        d_min = inf

        for i in range(len(points)):
            # skip the same point
            if p == points[i]:
                continue

            #compute distance
            dx = points[i].x() - p.x()
            dy = points[i].y() - p.y()
            d = sqrt(dx**2 + dy**2)

            # update minimum
            if d < d_min:
                d_min = d
                idx_min = i

        return points[idx_min]

    # update active edges list
    def updateAEL(self, e: Edge, AEL: list[Edge]):
        # get opposite edge
        eo = e.switchOrientation()

        # opposite edge in AEL
        if eo in AEL:
            AEL.remove(eo)
        else:
            AEL.append(e)

    # create Delaunay Triangulation
    def createDT(self, points: list[QPoint3DF]):
        # supplementary features
        dt: list[Edge] = []
        ael: list[Edge] = []

        # find pivot (minimum x)
        p1 = min(points, key=lambda k: k.x())

        # find nearest point
        p2 = self.getNearestPoint(p1, points)

        # create edge and opposite edge
        e = Edge(p1, p2)
        eo = Edge(p2, p1)

        # add edges to AEL
        ael.append(e)
        ael.append(eo)

        # process AEL until it is empty
        while ael:
            # take the first edge from AEL and switch its orientation
            e1 = ael.pop()
            e1o = e1.switchOrientation()

            # find Delaunay point
            idx = self.getDelaunayPoint(e1o.getStart(), e1o.getEnd(), points)

            # suitable point found
            if idx != -1:
                # create new edges
                e2 = Edge(e1o.getEnd(), points[idx])
                e3 = Edge(points[idx], e1o.getStart())

                # add edges to DT
                dt.append(e1o)
                dt.append(e2)
                dt.append(e3)

                # update AEL
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)

        return dt

    # get plane and line intersection
    def getContourLinePoint(self, p1: QPoint3DF, p2: QPoint3DF, z: float):
        xb = ((p2.x() - p1.x()) * (z - p1.getZ()) / (p2.getZ() - p1.getZ())) + p1.x()
        yb = ((p2.y() - p1.y()) * (z - p1.getZ()) / (p2.getZ() - p1.getZ())) + p1.y()

        return QPoint3DF(xb, yb, z)

    # create contour lines inside given interval with given step
    def createContourLines(self, dt: list[Edge], zmin: float, zmax: float, dz: float):
        contours: list[Edge] = []

        # process all triangles
        for i in range(0, len(dt), 3):
            # get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()

            # get elevations of the points
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()

            # test intersections of all planes
            for z in range(zmin, zmax, dz):
                # get height differences
                dz1 = z - z1
                dz2 = z - z2
                dz3 = z - z3

                # triangle is coplanar
                if (dz1 == 0) and (dz2 == 0) and (dz3 == 0):
                    continue

                # udělat z tohodle nebo jen vnitřku samostatnou metodu?
                # edges 1,2 and 2,3 are intersected by plane
                if (dz1 * dz2 <= 0) and (dz2 * dz3 <= 0):
                    # compute intersections and create contour line
                    a = self.getContourLinePoint(p1, p2, z)
                    b = self.getContourLinePoint(p2, p3, z)
                    contours.append(Edge(a, b))

                # edges 2,3 and 3,1 are intersected by plane
                elif (dz2 * dz3 <= 0) and (dz3 * dz1 <= 0):
                    # compute intersections and create contour line
                    a = self.getContourLinePoint(p2, p3, z)
                    b = self.getContourLinePoint(p3, p1, z)
                    contours.append(Edge(a, b))

                # edges 3,1 and 1,2 are intersected by plane
                elif (dz3 * dz1 <= 0) and (dz1 * dz2 <= 0):
                    # compute intersections and create contour line
                    a = self.getContourLinePoint(p3, p1, z)
                    b = self.getContourLinePoint(p1, p2, z)
                    contours.append(Edge(a, b))

        return contours

    # compute normal vector of triangle
    def getNomrVector(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        # first vector
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        uz = p2.getZ() - p1.getZ()

        # second vector
        vx = p3.x() - p1.x()
        vy = p3.y() - p1.y()
        vz = p3.getZ() - p1.getZ()

        # normal vector components
        nx = uy * vz - uz * vy
        ny = -(ux * vz - uz * vx)
        nz = ux * vy - uy * vx

        return nx, ny, nz

    def getSlope(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        #get normal vector
        nx, ny, nz = self.getNomrVector(p1, p2, p3)

        # norm
        n = sqrt(nx*nx + ny*ny + nz*nz)

        # return slope
        return acos(nz / n)

    # get triangle aspect
    def getAspect(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        # get normal vector
        nx, ny, nz = self.getNomrVector(p1, p2, p3)

        # return aspect
        aspect = atan2(ny, nx)

        if aspect < 0:
            return (aspect + 2 *pi)

        return aspect

    # analyze slope of triangles
    def analyzeDTMSlope(self, dt: list[Edge]):
        dtm: list[Triangle] = []

        # process all triangles
        for i in range(0, len(dt), 3):
            # get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()

            # compute slope
            slope = self.getSlope(p1, p2, p3)

            # create triangle and add it to list
            triangle = Triangle(p1, p2, p3, slope, -1)
            dtm.append(triangle)

        # return analyzed DTM
        return dtm

    # analyze aspect of triangles
    def analyzeDTMAspect(self, dt: list[Edge]):
        dtm: list[Triangle] = []

        # process all triangles
        for i in range(0, len(dt), 3):
            # get triangle vertices
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()

            # compute slope
            aspect = self.getAspect(p1, p2, p3)

            # create triangle and add it to list
            triangle = Triangle(p1, p2, p3, -1, aspect)
            dtm.append(triangle)

        # return analyzed DTM
        return dtm
