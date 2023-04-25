from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *
from edge import *
from triangle import *
from random import *
from math import pi
import csv

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # points, DT, contour lines, triangles
        self.__points: list[QPoint3DF] = []
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__emph_contours: list[Edge] = []
        self.__triangles: list[Triangle] = []

    # load data from input file
    def loadData(self, width, height):
        # get path to file via Dialog window
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "*.txt")
        path = filename[0]

        # return empty list of points if dialog window is closed
        if bool(filename[0]) == False:
            self.__points = []
            return self.__points

        # initialize lists of coordinates
        x_list = []
        y_list = []
        z_list = []

        # read file
        with open(path, "r") as f:
            for row in csv.reader(f, delimiter='\t'):
                # extract coordinates and convert them to float
                x_list.append(float(row[0]))
                y_list.append(float(row[1]))
                z_list.append(float(row[2]))

        # get min and max x, y coordinates
        min_max = [min(x_list), min(y_list), max(x_list), max(y_list)]

        # rescale data to fit the window of application
        for i in range(len(x_list)):
            x = int(((x_list[i] - min_max[0]) / (min_max[2] - min_max[0]) * width))
            y = int((height - (y_list[i] - min_max[1]) / (min_max[3] - min_max[1]) * (height)))
            p = QPoint3DF(x, y, z_list[i])
            self.__points.append(p)

    # get aspect color
    def getAspectColor(self, aspect):
        # North
        if (aspect >= 11*pi/8) and (aspect < 13*pi/8):
            return QColor(132, 214, 0)

        # Northeast
        elif (aspect >= 13*pi/8) and (aspect < 15*pi/8):
            return QColor(0, 171, 68)

        # East
        elif ((aspect >= 0) and (aspect < pi/8)) or ((aspect >= 15*pi/8) and (aspect < 2*pi)):
            return QColor(0, 104, 192)

        # Southeast
        elif (aspect >= pi/8) and (aspect < 3*pi/8):
            return QColor(108, 0, 163)

        # South
        elif (aspect >= 3*pi/8) and (aspect < 5*pi/8):
            return QColor(202, 0, 156)

        # Southwest
        elif (aspect >= 5*pi/8) and (aspect < 7*pi/8):
            return QColor(255, 85, 104)

        # West
        elif (aspect >= 7*pi/8) and (aspect < 9*pi/8):
            return QColor(255, 171, 71)

        # Northwest
        elif (aspect >= 9*pi/8) and (aspect < 11*pi/8):
            return QColor(244, 250, 0)

        else:
            return QColor(255, 255, 255)

    # draw points and analyses of DTM
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
                color = self.getAspectColor(aspect)
                qp.setBrush(color)

                # create new polygon
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])

            # draw polygon
            qp.drawPolygon(pol)

        # set attributes for triangles
        qp.setPen(Qt.GlobalColor.green)
        qp.setBrush(Qt.GlobalColor.transparent)

        # draw triangles
        for e in self.__dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # set attributes for contour lines
        qp.setPen(Qt.GlobalColor.darkRed)

        # draw contour lines
        for c in self.__contours:
            qp.drawLine(int(c.getStart().x()), int(c.getStart().y()), int(c.getEnd().x()), int(c.getEnd().y()))

        # set attributes for emphasized contour lines
        qp.setPen(QPen(Qt.GlobalColor.darkRed, 2))

        # draw emphasized contour lines
        for c in self.__emph_contours:
            qp.drawLine(int(c.getStart().x()), int(c.getStart().y()), int(c.getEnd().x()), int(c.getEnd().y()))

        # end draw
        qp.end()

    # set Delaunay triangulation
    def setDT(self, dt: list[Edge]):
        self.__dt = dt

    # set contour lines
    def setContours(self, contours: list[Edge], emph_contours: list[Edge]):
        self.__contours = contours
        self.__emph_contours = emph_contours

    # set triangles
    def setTriangles(self, dtm: list[Triangle]):
        self.__triangles = dtm

    # return list of points
    def getPoints(self):
        return self.__points

    # return Delaunay triangulation
    def getDT(self):
        return self.__dt

    # clear all results and points
    def clearAll(self):
        self.__points: list[QPoint3DF] = []
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__emph_contours: list[Edge] = []
        self.__triangles: list[Triangle] = []
        self.repaint()

    # clear results
    def clearResults(self):
        self.__dt: list[Edge] = []
        self.__contours: list[Edge] = []
        self.__emph_contours: list[Edge] = []
        self.__triangles: list[Triangle] = []
        self.repaint()