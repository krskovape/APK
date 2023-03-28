from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np

class Algorithms:
    def __init__(self):
        pass

    def getPointPolygonPosition(self, q, pol):
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
            return True
        return False

    def get2LinesAngle(self, p1: QPointF, p2: QPointF, p3: QPointF, p4: QPointF):
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

    def getPointLinePosition(self, p: QPointF, p1: QPointF, p2: QPointF):
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

    # compute lenght between two points
    def getLength(self, p1: QPointF, p2: QPointF):
        # compute vectors
        dx_i = p2.x() - p1.x()
        dy_i = p2.y() - p1.y()

        # compute length of the edge
        return sqrt(dx_i ** 2 + dy_i ** 2)

    # create convex hull using Jarvis scan
    def jarvisScan(self, pol: QPolygonF):
        # initialize convex hull
        ch = QPolygonF()

        # find pivot
        q = min(pol, key = lambda k : k.y())

        # initialize pj-1, pj
        pj1 = QPointF(q.x() - 1, q.y())
        pj = q

        # add q to convex hull
        ch.append(q)

        # Jarvis scan
        while True:
            # initialize maximum
            phi_max = 0
            i_max = -1

            # find suitable point maximizing angle
            for i in range(len(pol)):

                if pj != pol[i]:
                    # measure angle
                    phi = self.get2LinesAngle(pj, pj1, pj, pol[i])

                    # actualize phi_max
                    if phi > phi_max:
                        phi_max = phi
                        i_max = i

            # append point to CH
            ch.append(pol[i_max])

            # actualize last two points
            pj1 = pj
            pj = pol[i_max]

            # stop condition
            if pj == q:
                break

        return ch

    # create convex hull using Graham scan
    def grahamScan(self, pol:QPolygonF):
        # initialize convex hull
        ch = QPolygonF()

        # find pivot and parallel to x
        q = min(pol, key = lambda k : k.y())
        x_p = QPointF(q.x() + 10, q.y())

        # sort points by angle
        points = {}
        for i in range(len(pol)):
            # skip pivot
            if pol[i] == q:
                continue

            # compute angle
            omega = self.get2LinesAngle(q, x_p, q, pol[i])

            # store omega as key
            if omega in points.keys():
                # choose point further from pivot q
                idx = points[omega]
                l_in = self.getLength(q, pol[idx])
                l_om = self.getLength(q, pol[i])
                if l_om > l_in:
                    points[omega] = i
            else:
                points[omega] = i

        # sort points in S by omega
        points_sort = {k: points[k] for k in sorted(points)}

        # append pivot and first point to the stack
        S = []
        S.append(q)
        S.append(pol[list(points_sort.values())[0]])

        # process sorted points
        j = 1
        while j < len(points_sort):
            n = len(ch)
            # get point in sorted list
            pj = pol[list(points_sort.values())[j]]

            # get position of pj and last edge of the convex hull
            pos = self.getPointLinePosition(pj, S[-2], S[-1])

            # point in left halfplane, add point to convex hull
            if pos == 1:
                S.append(pj)
                j += 1

            # point in right halfplane, remove last node of convex hull
            else:
                S.pop()

        # add points from the stack to the convex hull
        for p in S:
            ch.append(p)

        return ch

    def rotate(self, pol: QPolygonF, sig: float) -> QPolygonF:
        # rotated polygon
        pol_rot = QPolygonF()

        # process all polygon vertices
        for i in range(len(pol)):
            # rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            # add point to rotated polygon
            vertex = QPointF(x_rot, y_rot)
            pol_rot.append(vertex)

        return pol_rot

    def minMaxBox(self, pol: QPolygonF):
        # find extreme coordinates
        # fce min vrací bod s min/max souřadnicí, musíme z něj vytáhnout ještě danou souřadnici
        x_min = min(pol, key= lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # create minmax box vertices
        v1 = QPointF(x_min, y_min)
        v2 = QPointF(x_max, y_min)
        v3 = QPointF(x_max, y_max)
        v4 = QPointF(x_min, y_max)

        # create minmax box from vertices
        minmax_box = QPolygonF([v1, v2, v3, v4])

        # compute minmax box area
        area = (x_max - x_min) * (y_max - y_min)

        return minmax_box, area

    def minAreaEnclosingRectangle(self, pol: QPolygonF, ch):
        # get minmax box and area
        mmb_min, area_min = self.minMaxBox(ch)
        sigma_min = 0

        # process all segments of ch
        for i in range(len(ch)-1):
            dx = ch[i+1].x() - ch[i].x()
            dy = ch[i+1].y() - ch[i].y()
            sigma = atan2(dy, dx)

            # rotate convex hull
            ch_rot = self.rotate(ch, -sigma)

            # find MMB of rotated convex hull
            mmb, area = self.minMaxBox(ch_rot)

            # update minimum MMB
            if area < area_min:
                area_min = area
                mmb_min = mmb
                sigma_min = sigma

        # rotate MMB
        er = self.rotate(mmb_min, sigma_min)

        # resize rectangle
        er_res = self.resizeRectangle(er, pol)

        return er_res

    def computeArea(self, pol: QPolygonF):
        # compute area
        n = len(pol)
        area = 0

        # process all vertices
        for i in range(n):
            # increment area
            area += pol[i].x() * (pol[(i+1) % n].y() - pol[(i-1+n) % n].y())

        return 0.5 * abs(area)

    def resizeRectangle(self, er: QPolygonF, pol: QPolygonF):

        # compute area of building and enclosing rectangle
        ab = abs(self.computeArea(pol))
        a = abs(self.computeArea(er))

        print(f"building: {ab}")
        print(f"er: {a}")

        # fraction of building and ER area
        k = ab / a

        n_er = len(er)
        pol_res = QPolygonF()

        # center of mass of enclosing rectangle
        x_er = 0
        y_er = 0
        for i in range(n_er):
            x_er += er[i].x()
            y_er += er[i].y()
        x_t = x_er / n_er
        y_t = y_er / n_er

        # compute vectors and nex vertices
        for i in range(n_er):
            #compute vector
            u_x = er[i].x() - x_t
            u_y = er[i].y() - y_t

            # compute coordinates of new vertex
            v_x = x_t + sqrt(k) * u_x
            v_y = y_t + sqrt(k) * u_y

            # create new vertex and append it to resized polygon
            v = QPointF(v_x, v_y)
            pol_res.append(v)

        ar = abs(self.computeArea(pol_res))
        print(f"er res: {ar}")

        # return reduced enclosing rectangle
        return pol_res

    def wallAverage(self, pol: QPolygonF):
        # compute sigma
        dx = pol[1].x() - pol[0].x()
        dy = pol[1].y() - pol[0].y()
        sigma = atan2(dy, dx)

        # process all edges
        n = len(pol)

        r_aver = 0

        for i in range(1, n):
            # compute sigma i
            dx_i = pol[(i+1)%n].x() - pol[i].x()
            dy_i = pol[(i+1)%n].y() - pol[i].y()
            sigma_i = atan2(dy_i, dx_i)

            # direction difference
            d_sigma_i = sigma_i - sigma

            # correct delta sigma i
            if d_sigma_i < 0:
                d_sigma_i += 2*pi

            # fraction
            ki = round((2*d_sigma_i) / pi)

            # remainder
            ri = d_sigma_i - (ki * pi/2)

            # average remainder
            r_aver += ri

        # average remainder
        r_aver = r_aver / n

        # average direction
        sigma_aver = sigma + r_aver

        # rotate building
        pol_rot = self.rotate(pol, -sigma_aver)

        # find MMB of rotated building
        mmb, area = self.minMaxBox(pol_rot)

        # rotate MMB
        er = self.rotate(mmb, sigma_aver)

        # resize building
        er_r = self.resizeRectangle(er, pol)

        return er_r

    def longestEdge(self, pol: QPolygonF):
        # process all edges
        n = len(pol)
        len_max = 0

        for i in range(n):
            # get length of the edge
            len_e = self.getLength(pol[i], pol[(i + 1) % n])

            if len_e > len_max:
                len_max = len_e
                sigma = atan2(pol[(i + 1) % n].y() - pol[i].y(), pol[(i + 1) % n].x() - pol[i].x())

        # rotate building
        pol_rot = self.rotate(pol, -sigma)

        # find MMB of rotated building
        mmb, area = self.minMaxBox(pol_rot)

        # rotate MMB
        er = self.rotate(mmb, sigma)

        # resize building
        er_r = self.resizeRectangle(er, pol)

        return er_r

    def principalComponent(self, pol: QPolygonF):
        # compute matrix of all nodes
        A = []
        for i in range(len(pol)):
            A.append([pol[i].x(),pol[i].y()])
        print(A)

        # singular value decomposition
        U, s, VT = np.linalg.svd(A)

        # compute vectors and sigma
        vectors = VT.transpose()
        v1 = vectors[0][0]
        v2 = vectors[0][1]
        sigma = atan2(v2, v1)

        # rotate building
        pol_rot = self.rotate(pol, -sigma)

        # find MMB of rotated building
        mmb, area = self.minMaxBox(pol_rot)

        # rotate MMB
        er = self.rotate(mmb, sigma)

        # resize building
        er_r = self.resizeRectangle(er, pol)

        return er_r

    def weightedBisector(self, pol: QPolygonF):
        n = len(pol)
        diag_1 = [None, None, 0]
        diag_2 = [None, None, 0]

        for i in range(n):
            for j in range(n):
                # skip computing length between the same point
                if pol[i] == pol[j]:
                    continue

                # check if the diagonal doesn´t cross any edge
                inter = True
                for k in range(n):
                    # compute vectors
                    x1 = pol[i].x()
                    y1 = pol[i].y()
                    x2 = pol[j].x()
                    y2 = pol[j].y()
                    x3 = pol[k].x()
                    y3 = pol[k].y()
                    x4 = pol[(k + 1) % n].x()
                    y4 = pol[(k + 1) % n].y()

                    # compute determinants
                    t1 = (x2 - x1) * (y4 - y1) - (x4 - x1) * (y2 - y1)
                    t2 = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
                    t3 = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)
                    t4 = (x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3)

                    # check for the intersection
                    if (t1 * t2 < 0) or (t3 * t4 < 0):
                        inter = False
                        break

                # diagonal doesn´t cross any edge
                if inter:
                    # compute length of the diagonal
                    s = self.getLength(pol[i], pol[j])

                    # update two longest diagonals
                    if s > diag_1[2]:
                        diag_1[0] = pol[i]
                        diag_1[1] = pol[j]
                        diag_1[2] = s
                    elif s > diag_2[2]:
                        diag_2[0] = pol[i]
                        diag_2[1] = pol[j]
                        diag_2[2] = s

        # compute angles for diagonals
        sigma_1 = atan2(diag_1[1].y() - diag_1[1].y(), diag_1[1].x() - diag_1[1].x())
        sigma_2 = atan2(diag_2[1].y() - diag_2[1].y(), diag_2[1].x() - diag_2[1].x())

        # compute angle for rotation of the building
        s1 = diag_1[2]
        s2 = diag_2[2]
        sigma = (s1 * sigma_1 + s2 * sigma_2) / (s1 + s2)

        # rotate building
        pol_rot = self.rotate(pol, -sigma)

        # find MMB of rotated building
        mmb, area = self.minMaxBox(pol_rot)

        # rotate MMB
        er = self.rotate(mmb, sigma)

        # resize building
        er_r = self.resizeRectangle(er, pol)

        return er_r