from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # buildings, convex hull and enclosing rectangle
        self.__polygons = []
        self.__features = None
        self.__min_max = [0, 0, 10, 10]
        self.__no_data = False
        self.__pol = QPolygonF()
        self.__ch = QPolygonF()
        self.__er = []

    # function for loading input data
    def loadData(self):
        # get path to file via Dialog window
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")
        path = filename[0]

        # update no data property to draw hidden polygon if dialog window is closed
        if bool(filename[0]) == False:
            self.__no_data = True
            return
        self.__no_data = False

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

    # rescale data to fit Canvas
    def rescaleData(self, width, height):
        # construct hidden polygon
        if self.__no_data == True:
            self.__polygons = []
            pol = QPolygonF([QPointF(0, 0), QPointF(-10, 0), QPointF(0, -10), QPointF(-10, -10)])
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
                    y = int((height - (point[1] - self.__min_max[1]) / (self.__min_max[3] - self.__min_max[1]) * (
                        height)))
                    p = QPointF(x, y)
                    self.__polygons[k].append(p)

    # left mouse button click
    def mousePressEvent(self, e:QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()

        # add point to polygon
        p = QPointF(x,y)
        self.__pol.append(p)

        # repaint screen
        self.repaint()

    # draw polygon
    def paintEvent(self, e: QPaintEvent):
        # create graphic object
        qp = QPainter(self)

        # start draw
        qp.begin(self)

        # # set attributes for building
        # qp.setPen(Qt.GlobalColor.black)
        # qp.setBrush(Qt.GlobalColor.white)
        #
        # # draw building
        # qp.drawPolygon(self.__pol)
        for index, polygon in enumerate(self.__polygons):
            # set attributes
            qp.setPen(QColor.fromString("steelblue"))
            qp.setBrush(QColor.fromString("powderblue"))
            qp.drawPolygon(polygon)

        # set attributes for convex hull
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.yellow)

        # draw convex hull
        qp.drawPolygon(self.__ch)

        for index, er in enumerate(self.__er):
            # set attributes for enclosing rectangle
            qp.setPen(Qt.GlobalColor.red)
            qp.setBrush(Qt.GlobalColor.green)

            # draw enclosing rectangle
            qp.drawPolygon(er)
        self.__er = []

        # # set attributes for building
        # qp.setPen(Qt.GlobalColor.black)
        # qp.setBrush(Qt.GlobalColor.transparent)
        #
        # # draw building
        # qp.drawPolygon(self.__pol)

        # end draw
        qp.end()

    # get polygon
    def getPolygon(self):
        return self.__pol

    # set polygon as convex hull
    def setCH(self, pol: QPolygonF):
        self.__ch = pol

    # set polygon as enclosing rectangle
    def setER(self, pol: QPolygonF):
        self.__er.append(pol)

    def cleanCanvas(self):
        self.__polygons = []
        self.__ch = []
        self.__er = []
        self.repaint()

    def getPolygons(self):
        return self.__polygons
