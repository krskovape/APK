from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # query point and polygon - F for float numbers
        self.__q = QPointF(-10,-10)
        self.__pol = QPolygonF()
        self.__polygons = []

        self.__add_vertex = True

    def loadFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")
        path = filename[0]

        shapef = shapefile.Reader(path)
        features = shapef.shapes()

        self.__polygons = [None] * len(shapef)

        for k in range(len(shapef)):
            self.__polygons[k] = QPolygonF()
            for point in features[k].points:
                x = point[0]
                y = point[1]
                p = QPointF(x,y)
                self.__polygons[k].append(p)
        return self.__polygons


    # left mouse button click
    def mousePressEvent(self, e:QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()

        # add point to polygon
        if self.__add_vertex == True:
            # create point, add point to polygon
            p = QPointF(x,y)
            self.__pol.append(p)
        # set x,y to point
        else:
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

        # set attributes
        qp.setPen(Qt.GlobalColor.darkGreen)
        qp.setBrush(Qt.GlobalColor.yellow)

        # draw polygon
        for polygon in self.__polygons:
            qp.drawPolygon(polygon)

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
    def getPolygon(self):
        return self.__pol