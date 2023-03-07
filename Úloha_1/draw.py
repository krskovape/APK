from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile
from math import inf

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # query point, lists for storing polygons and their results of analysis
        self.__q = QPointF(-10,-10)
        self.__polygons = []
        self.__pol_res = []

    # function for loading file
    def loadFile(self, width, height):
        # get path to file via Dialog window
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")
        path = filename[0]

        # return previous polygons if dialog window is closed
        if bool(filename[0]) == False:
            return self.__polygons

        # load objects from shapefile
        shp = shapefile.Reader(path)
        features = shp.shapes()

        # find minimum and maximum of the coordinates
        x_lst = []
        y_lst = []
        for k in range(len(shp)):
            for point in features[k].points:
                x_lst.append(point[0])
                y_lst.append(point[1])
        maxc_x = max(x_lst)
        maxc_y = max(y_lst)
        minc_x = min(x_lst)
        minc_y = min(y_lst)

        # initialize list for storing polygons
        self.__polygons = [None] * len(shp)

        # rescale data and create polygons
        for k in range(len(shp)):
            self.__polygons[k] = QPolygonF()
            for point in features[k].points:
                x = int(((point[0]-minc_x)/(maxc_x-minc_x)*width))
                y = int((height - (point[1]-minc_y)/(maxc_y-minc_y)*(height)))
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

            # set diferent color for polygons containing point
            if self.__pol_res and (self.__pol_res[index] == 1) or self.__pol_res and (self.__pol_res[index] == -1):
                qp.setPen(QColor.fromString("green"))
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
