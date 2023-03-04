from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from math import sqrt, acos, pi

class Algorithms:
    def __init__(self):
        pass

    def getPointAndEdgePosition(self, q, p1: QPointF, p2: QPointF):
        # compute vectors
        v1_x = q.x() - p1.x()
        v1_y = q.y() - p1.y()
        v2_x = p2.x() - p1.x()
        v2_y = p2.y() - p1.y()

        # compute determinant
        d = (v1_x * v2_y) - (v2_x * v1_y)

        # determine point and edge position
        # point in left halfplane
        if d > 0:
            return 1

        # point in right halfplace
        elif d < 0:
            return 0

        # colinear point
        return -1

    def getAngle(self, q, p1: QPointF, p2: QPointF):
        # compute vectors
        v1_x = p1.x() - q.x()
        v1_y = p1.y() - q.y()
        v2_x = p2.x() - q.x()
        v2_y = p2.y() - q.y()

        # compute the scalar product of vectors
        v1v2 = v1_x * v2_x + v1_y * v2_y

        # compute the norms of vectors
        norm_v1 = sqrt(v1_x**2 + v1_y**2)
        norm_v2 = sqrt(v2_x ** 2 + v2_y ** 2)

        # point lies on the edge
        if norm_v1 == 0 or norm_v2 == 0:
            return -1

        # compute angle
        return acos(v1v2 / (norm_v1 * norm_v2))

    def windingNumber(self, q, pol):
        # initialize sum of omega and tolerance
        omega_sum = 0
        epsilon = 1.0e-10

        # loop through polygon
        for i in range(len(pol)-1):
            # get position of point and edge
            pos = self.getPointAndEdgePosition(q, pol[i], pol[i+1])

            # get angle between point and vertices of the edge
            omega = self.getAngle(q, pol[i], pol[i+1])

            # point in left halfplane
            if pos == 1:
                omega_sum += omega

            # point in right halfplane
            if pos == 0:
                omega_sum -= omega

        if abs(abs(omega_sum) - 2*pi) < epsilon:
            return 1
        else: return 0

    def RayCrossing(self, q, pol):
        # počet průsečíků (k), number of vertices (n)
        k = 0
        n = len(pol)

        # process all vertices
        for i in range(n):
            # reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            # modulo (%n), abychom nepřekročili index, poslední bod bude zase ten první
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()

            # suitable segment - protnutý horizontálním paprskem, oba konce v jiných polorovinách nebo...
            if yi1r > 0 and yir <= 0 or yir > 0 and yi1r <= 0:
                # compute intersection
                xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)

                # increment amount of intersections
                if xm > 0:
                    k += 1

        # point is inside
        if k % 2 == 1:
            return 1
        return 0