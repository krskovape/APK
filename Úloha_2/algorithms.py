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

    def createCH(self, pol:QPolygonF):
        #Create CH using Jarvis scan
        ch = QPolygonF()

        #Find pivot
        q = min(pol, key = lambda k : k.y())

        #Initialize pj-1, pj
        pj1 = QPointF(q.x() - 1, q.y())
        pj = q

        #Add q to convex hull
        ch.append(q)

        # Jarvis scan
        while True:
            #Initialize maximum
            phi_max = 0
            i_max = -1

            #Find suitable point maximizing angle
            for i in range(len(pol)):

                if pj != pol[i]:
                    #Measure angle
                    phi = self.get2LinesAngle(pj, pj1, pj, pol[i])

                    #Actualize phi_max
                    if phi > phi_max:
                        phi_max = phi
                        i_max = i

            # Append point to CH
            ch.append(pol[i_max])

            #Actualize last two points
            pj1 = pj
            pj = pol[i_max]

            # Stop condition
            if pj == q:
                break

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

    def minAreaEnclosingRectangle(self, pol: QPolygonF):
        # create convex hull
        ch = self.createCH(pol)

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
            # compute sigma i
            dx_i = pol[(i + 1) % n].x() - pol[i].x()
            dy_i = pol[(i + 1) % n].y() - pol[i].y()
            sigma_i = atan2(dy_i, dx_i)

            # compute length of the edge
            len_e = sqrt(dx_i **2 + dy_i **2)

            if len_e > len_max:
                len_max = len_e
                index = i
                sigma = sigma_i

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