from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from numpy import *

class Algorithms:
    def __init__(self):
        pass

    # compute euclidean distance between two points
    def getEuclDistance(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return sqrt(dx**2 + dy**2)

    # compute distance between point A=[xa, ya] and line (p1, p2)
    def getPointLineDistance(self, xa, ya, x1, y1, x2, y2):
        # compute distance
        dn = xa * (y1 - y2) + x1 * (y2 - ya) + x2 * (ya - y1)
        dd = self.getEuclDistance(x1, y1, x2, y2)
        d = dn / dd

        # get coordinates of point Q
        d1 = self.getEuclDistance(x1, y1, xa, ya)
        k = sqrt(d1**2 - d**2)
        xq = x1 + k * (x2 - x1) / dd
        yq = y1 + k * (y2 - y1) / dd

        return d, xq, yq

    # compute distance between point A=[xa, ya] and line segment (p1, p2)
    def getPointSegmentDistance(self, xa, ya, x1, y1, x2, y2):
        # direction vector
        ux = x2 - x1
        uy = y2 - y1

        # normal vector
        nx = -uy
        ny = ux

        # point p3, p4
        x3 = x1 + nx
        y3 = y1 + ny
        x4 = x2 + nx
        y4 = y2 + ny

        # posisiotn of A according to (p1, p3) and (p2, p4)
        d13, xq3, yq3 = self.getPointLineDistance(xa, ya, x1, y1, x3, y3)
        d24, xq4, yq4 = self.getPointLineDistance(xa, ya, x2, y2, x4, y4)

        # point between two normals
        t = d13 * d24
        if t < 0:
            d, xq, yq = self.getPointLineDistance(xa, ya, x1, y1, x2, y2)
            return abs(d), xq, yq

        # point in the left halfplane
        if d13 > 0:
            return self.getEuclDistance(xa, ya, x1, y1), x1, y1

        # point in the right halfplane
        return self.getEuclDistance(xa, ya, x2, y2), x2, y2

    # get point on the barrier nearest to point A
    def getNearestLineSegmentPoint(self, xa : float , ya : float, X: matrix, Y: matrix):
        # initialize minimum distance and index of point
        dmin = inf
        imin = -1

        # size of the matrix
        m, n = X.shape

        # browse all line segments
        for i in range(m-1):
            # compute distance between point A=[xa, ya] and line segment (p[i], p[i+1])
            di, xi, yi = self.getPointLineDistance(xa, ya, X[i,0], Y[i,0], X[i+1,0], Y[i+1,0])

            # update minimum
            if di < dmin:
                dmin = di
                imin = i
                xmin = xi
                ymin = yi

        return dmin, imin, xmin, ymin

    # create matrix A
    def createA(self, alpha, beta, gamma, h, m):
        # coefficients a, b, c
        a = alpha + (2 * beta) / h**2 + (6 * gamma) / h**4
        b = -beta / h**2 - (4 * gamma) / h**4
        c = gamma / h**4

        # create matrix
        A = zeros((m,m))

        for i in range(m):
            # main diagonal element
            A[i,i] = a

            # non-diagonal elements, test
            if i < (m-1):
                A[i, i+1] = b
                A[i+1, i] = b
            if i < (m-2):
                A[i, i+2] = c
                A[i+2, i] = c

        return A

    def getEx(self, xi, yi, xn, yn, d, dmin):
        # partial derivative of the outer energy according to x
        c = 20 * dmin

        # vertex is closer than minimum distance
        if d < dmin:
            return -c * (xi - xn) / (dmin * d)

        return 0

    def getEy(self, xi, yi, xn, yn, d, dmin):
        # partial derivative of the outer energy according to y
        c = 20 * dmin

        # vertex is closer than minimum distance
        if d < dmin:
            return -c * (yi - yn) / (dmin * d)

        return 0

    def minEnergySpline(self, L: list[QPointF], B: list[QPointF], alpha: float, beta: float, gamma: float,
                        lam: float, dmin: float, iters):
        # minimum energy spline
        ml = len(L)
        mb = len(B)

        # create empty matrices
        XL = zeros((ml, 1))
        YL = zeros((ml, 1))
        XB = zeros((mb, 1))
        YB = zeros((mb, 1))

        # convert polyline to matrix representation
        for i in range(ml):
            XL[i, 0] = L[i].x()
            YL[i, 0] = L[i].y()

        # convert barrier to matrix representation
        for i in range(mb):
            XB[i, 0] = B[i].x()
            YB[i, 0] = B[i].y()

        # compute step h
        dx = transpose(diff(transpose(XL)))
        dy = transpose(diff(transpose(YL)))

        H = sqrt(multiply(dx, dx) + multiply(dy, dy))
        h = H.mean()

        # create A
        A = self.createA(alpha, beta, gamma, h, ml)

        # compute inverse matrix
        I = identity(ml)
        AI = linalg.inv(A + lam * I)

        # create difference matrices
        DX = zeros((ml, 1))
        DY = zeros((ml, 1))

        # displaced vertices
        XLi = XL
        YLi = YL

        # main iteration process
        for i in range(iters):
            # partial derivatives of potentials according to dx, dy
            Ex = zeros((ml, 1))
            Ey = zeros((ml, 1))

            # compute Ex, Ey
            for j in range(0, ml):
                # find nearest point
                dn, idxn, xn, yn = self.getNearestLineSegmentPoint(XLi[j, 0], YLi[j, 0], XB, YB)

                # compute EX, Ey
                Ex[j, 0] = self.getEx(XLi[j, 0], YLi[j, 0], xn, yn, dn, dmin)
                Ey[j, 0] = self.getEy(XLi[j, 0], YLi[j, 0], xn, yn, dn, dmin)

            # compute shifts
            DX = AI @ (lam * DX - Ex)
            DY = AI @ (lam * DY - Ey)

            XLi = XL + DX
            YLi = YL + DY

        # convert matrix representation to polyline
        LD = []
        for j in range(ml):
            v = QPointF(XLi[j, 0], YLi[j, 0])
            LD.append(v)

        return LD