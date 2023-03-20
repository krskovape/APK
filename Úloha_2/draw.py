from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # buildings, convex hull and enclosing rectangle
        self.__pol = QPolygonF()
        self.__ch = QPolygonF()
        self.__er = QPolygonF()

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

        # set attributes for building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.white)

        # draw building
        qp.drawPolygon(self.__pol)

        # set attributes for convex hull
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.yellow)

        # draw convex hull
        qp.drawPolygon(self.__ch)

        # set attributes for enclosing rectangle
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.green)

        # draw enclosing rectangle
        qp.drawPolygon(self.__er)

        # set attributes for building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.transparent)

        # draw building
        qp.drawPolygon(self.__pol)

        # end draw
        qp.end()

    def switchSource(self):
        # move point or add vertex (negace přes not)
        self.__add_vertex = not(self.__add_vertex)

    # get polygon
    def getPolygon(self):
        return self.__pol

    # set polygon as convex hull
    def setCH(self, pol: QPolygonF):
        self.__ch = pol

    # set polygon as enclosing rectangle
    def setER(self, pol: QPolygonF):
        self.__er = pol

    def cleanCanvas(self):
        self.__pol = []
        self.__ch = []
        self.__er = []
        self.repaint()
