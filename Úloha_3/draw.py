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

        # draw aspect
        k = 510 / pi

        # process all triangles
        for t in self.__triangles:
            # get slope
            slope = t.getSlope()

            # convert to color
            col = 255 - int(slope * k)

            # create color
            color = QColor(col, col, col)
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

    def setSlope(self, dtm: list[Triangle]):
        self.__triangles = dtm

    def getPoints(self):
        return self.__points

    def getDT(self):
        return self.__dt