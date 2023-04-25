from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from edge import *
from triangle import *
from random import *
from math import pi

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # points, DT, contour lines, triangles
        self.__points: list[QPoint3DF] = []
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []

    # left mouse button click
    def mousePressEvent(self, e:QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()
        z = random() * 100

        # add point to points
        p = QPoint3DF(x,y,z)
        self.__points.append(p)

        # repaint screen
        self.repaint()

    def getAspectColor(self, aspect):
        # North
        if (aspect >= 11*pi/8) and (aspect < 13*pi/8):
            col1= 132
            col2 = 214
            col3 = 0

        # Northeast
        elif (aspect >= 13*pi/8) and (aspect < 15*pi/8):
            col1 = 0
            col2 = 171
            col3 = 68

        # East
        elif ((aspect >= 0) and (aspect < pi/8)) or ((aspect >= 15*pi/8) and (aspect < 2*pi)):
            col1 = 0
            col2 = 104
            col3 = 192

        # Southeast
        elif (aspect >= pi/8) and (aspect < 3*pi/8):
            col1 = 108
            col2 = 0
            col3 = 163

        # South
        elif (aspect >= 3*pi/8) and (aspect < 5*pi/8):
            col1 = 202
            col2 = 0
            col3 = 156

        # Southwest
        elif (aspect >= 5*pi/8) and (aspect < 7*pi/8):
            col1 = 255
            col2 = 85
            col3 = 104

        # West
        elif (aspect >= 7*pi/8) and (aspect < 9*pi/8):
            col1 = 255
            col2 = 171
            col3 = 71

        # Northwest
        elif (aspect >= 9*pi/8) and (aspect < 11*pi/8):
            col1 = 244
            col2 = 250
            col3 = 0

        return col1, col2, col3

    # draw polygon
    def paintEvent(self, e: QPaintEvent):
        # create graphic object
        qp = QPainter(self)

        # start draw
        qp.begin(self)

        # set attributes for points
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # draw points
        d = 5
        for p in self.__points:
            qp.drawEllipse(int(p.x() - d / 2), int(p.y() - d / 2), d, d)

        # draw slope or aspect
        k = 510 / pi

        # process all triangles
        for t in self.__triangles:
            # get slope and aspect
            slope = t.getSlope()
            aspect = t.getAspect()

            # draw slope
            if aspect == -1:
                # convert to color
                col = 255 - int(slope * k)

                # create color
                color = QColor(col, col, col)
                qp.setBrush(color)

                # create new polygon
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            # draw aspect
            else:
                # get aspect color
                col1, col2, col3 = self.getAspectColor(aspect)

                # create color
                color = QColor(col1, col2, col3)
                qp.setBrush(color)

                # create new polygon
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            # draw polygon
            qp.drawPolygon(pol)

        # set attributes for triangles
        qp.setPen(Qt.GlobalColor.green)
        qp.setBrush(Qt.GlobalColor.transparent)

        # draw contour triangles
        for e in self.__dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # set attributes for contour lines
        qp.setPen(Qt.GlobalColor.darkRed)
        #qp.setBrush(Qt.GlobalColor.white)

        # draw contour lines
        for c in self.__contours:
            qp.drawLine(int(c.getStart().x()), int(c.getStart().y()), int(c.getEnd().x()), int(c.getEnd().y()))

        # end draw
        qp.end()

    def setDT(self, dt: list[Edge]):
        self.__dt = dt

    def setContours(self, contours: list[Edge]):
        self.__contours = contours

    def setTriangles(self, dtm: list[Triangle]):
        self.__triangles = dtm

    def getPoints(self):
        return self.__points

    def getDT(self):
        return self.__dt

    def clearAll(self):
        self.__points: list[QPoint3DF] = []
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []
        self.repaint()

    def clearResults(self):
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__triangles: list[Triangle] = []
        self.repaint()