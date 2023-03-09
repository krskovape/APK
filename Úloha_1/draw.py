from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile
from math import inf

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize properties
        self.__q = QPointF(-10,-10)
        self.__polygons = []
        self.__pol_res = []
        self.__features = None
        self.__min_max = [0,0,10,10]
        self.__no_data = False

    # function for loading file
    def loadData(self):
        # get path to file via Dialog window
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")
        path = filename[0]

        # update no data property to draw hidden polygon if dialog window is closed
        if bool(filename[0]) == False:
            self.__no_data = True
            return

        # load objects from shapefile
        shp = shapefile.Reader(path)
        self.__features = shp.shapes()

        # find minimum and maximum of the coordinates
        x_lst = []
        y_lst = []
        for k in range(len(shp)):
            for point in self.__features[k].points:
                x_lst.append(point[0])
                y_lst.append(point[1])
        self.__min_max = [min(x_lst), min(y_lst), max(x_lst), max(y_lst)]

    def rescaleData(self, width, height):
        # construct hidden polygon
        if self.__no_data == True:
            self.__polygons = []
            pol = QPolygonF()
            pol.append(QPointF(0,0)); pol.append(QPointF(-10,0)); pol.append(QPointF(0,-10)); pol.append(QPointF(-10,-10))
            self.__polygons.append(pol)

        # rescale data
        else:
            # initialize list for storing polygons
            self.__polygons = [None] * len(self.__features)

            # rescale data and create polygons
            for k in range(len(self.__features)):
                self.__polygons[k] = QPolygonF()
                for point in self.__features[k].points:
                    x = int(((point[0] - self.__min_max[0]) / (self.__min_max[2] - self.__min_max[0]) * width))
                    y = int((height - (point[1] - self.__min_max[1]) / (self.__min_max[3] - self.__min_max[1]) * (height)))
                    p = QPointF(x,y)
                    self.__polygons[k].append(p)

    # left mouse button click
    def mousePressEvent(self, e:QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()

        # add point to polygon
        self.__q.setX(x)
        self.__q.setY(y)

        # repaint screen
        self.repaint()

    # draw polygon
    def paintEvent(self, e: QPaintEvent):
        # create graphic object
        qp = QPainter(self)

        # start draw
        qp.begin(self)

        # draw polygon
        for index, polygon in enumerate(self.__polygons):
            # set attributes
            qp.setPen(QColor.fromString("steelblue"))
            qp.setBrush(QColor.fromString("powderblue"))

            # set diferent color for polygons containing point or with point on its edge
            if self.__pol_res and (self.__pol_res[index] == 1) or self.__pol_res and (self.__pol_res[index] == -1):
                qp.setPen(QColor.fromString("steelblue"))
                qp.setBrush(QColor.fromString("yellowgreen"))

            qp.drawPolygon(polygon)

        self.__pol_res = []

        # set attributes for point
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.red)

        # draw point
        d = 8
        qp.drawEllipse(int(self.__q.x() - d/2), int(self.__q.y() - d/2), d, d)

        # end draw
        qp.end()

    # append result to list
    def setResult(self, result):
        self.__pol_res.append(result)

    # clear all polygons
    def clearPol(self):
        self.__polygons = []
        self.__q.setX(-10)
        self.__q.setY(-10)
        self.repaint()

    # get point
    def getPoint(self):
        return self.__q

    # get polygon
    def getPolygons(self):
        return self.__polygons
