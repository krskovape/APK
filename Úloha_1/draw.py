from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile
from math import inf

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # query point and polygon - F for float numbers
        self.__q = QPointF(-10,-10)
        self.__polygons = []
        self.__pol_index = []

        self.__draw_point = True

    def loadFile(self, width, height):
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")
        path = filename[0]

        shapef = shapefile.Reader(path)
        features = shapef.shapes()

        minc_x = inf
        minc_y = inf
        maxc_x = -inf
        maxc_y = -inf
        for f in features:
            min_x = min(f.points)[0]
            min_y = min(f.points)[1]
            max_x = max(f.points)[0]
            max_y = max(f.points)[1]
            if min_x < minc_x:
                minc_x = min_x
            if min_y < minc_y:
                minc_y = min_y
            if max_x > maxc_x:
                maxc_x = max_x
            if max_y > maxc_y:
                maxc_y = max_y

        self.__polygons = [None] * len(shapef)

        for k in range(len(shapef)):
            self.__polygons[k] = QPolygonF()
            for point in features[k].points:
                x = int(round((point[0]-minc_x)/(maxc_x-minc_x)*width))
                y = int(round(height - (point[1]-minc_y)/(maxc_y-minc_y)*height))
                p = QPointF(x,y)
                self.__polygons[k].append(p)


    # left mouse button click
    def mousePressEvent(self, e:QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()

        # add point to polygon
        if self.__draw_point == True:
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
            qp.setPen(Qt.GlobalColor.darkGreen)
            qp.setBrush(Qt.GlobalColor.yellow)

            if self.__pol_index and (self.__pol_index[index] == 1):
                qp.setPen(Qt.GlobalColor.magenta)
                qp.setBrush(Qt.GlobalColor.magenta)

            qp.drawPolygon(polygon)

        #self.__pol_index = []

        # set attributes for point
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.red)

        # draw point - zkusit místo toho drawPoint?
        d = 10
        qp.drawEllipse(int(self.__q.x() - d/2), int(self.__q.y() - d/2), d, d)

        # end draw
        qp.end()

    def switchSource(self):
        # move point or add vertex (negace přes not)
        self.__add_vertex = not(self.__add_vertex)

    # get point
    def getPoint(self):
        return self.__q

    # get polygon
    def getPolygons(self):
        return self.__polygons