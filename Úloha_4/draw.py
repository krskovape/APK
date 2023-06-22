from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import csv
from math import inf

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # line, barrier and displaced line
        self.__add_L = True
        self.__L = QPolygonF()
        self.__B = QPolygonF()
        self.__LD = QPolygonF()
        self.__min_max = []
        self.__xmin = inf
        self.__xmax = -inf
        self.__ymin = inf
        self.__ymax = -inf
        self.__L_is_rescaled = True
        self.__B_is_rescaled = True

    # load data from input file
    def loadData(self, width, height):
        # get path to file via Dialog window
        filename = QFileDialog.getOpenFileName(self, "Open file", "", "*.txt")
        path = filename[0]

        # return loaded L and B if dialog window is closed
        if bool(filename[0]) == False:
            if self.__add_L:
                return self.__L

            # add point to B
            else:
                return self.__B

        # read file
        with open(path, "r", encoding='utf-8-sig') as f:
            for row in csv.reader(f, delimiter=';'):
                # extract coordinates and convert them to float
                x = float(row[0])
                y = float(row[1])
                p = QPointF(x, y)
                self.findMinMax(p)

                # add point to L
                if self.__add_L:
                    self.__L.append(p)
                    self.__L_is_rescaled = False

                # add point to B
                else:
                    self.__B.append(p)
                    self.__B_is_rescaled = False

        self.resizeCanvas(height, width)
        self.repaint()

    # adjusts minimum and maximum coordinates of bounding box
    def findMinMax(self, p: QPointF):
        if p.x() < self.__xmin:
            self.__xmin = p.x()
        if p.y() < self.__ymin:
            self.__ymin = p.y()
        if p.x() > self.__xmax:
            self.__xmax = p.x()
        if p.y() > self.__ymax:
            self.__ymax = p.y()

    # resize and center input data to fit to display
    def resizeCanvas(self, height, width):
        # constant for window padding
        C = 100
        canvas_height = height - C
        canvas_width = width - C

        # swap xmin and xmax according to Krovak
        xmin = self.__xmax
        xmax = self.__xmin

        # rescale coordinates of line
        if not self.__L_is_rescaled:
            if (self.__ymax - self.__ymin) / canvas_height > (self.__xmax - self.__xmin) / canvas_width:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + C
                    new_y = int((point.y() - self.__ymin) * canvas_height / (self.__ymax - self.__ymin)) + C / 2

                    # reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.__L_is_rescaled = True
            else:
                for point in self.__L:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + C
                    new_y = int((point.y() - self.__ymin) * canvas_height / (self.__ymax - self.__ymin)) + C / 2

                    # reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.__L_is_rescaled = True

        # rescale coordinates of barrier
        if not self.__B_is_rescaled:
            if (self.__ymax - self.__ymin) / canvas_height > (self.__xmax - self.__xmin) / canvas_width:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_height / (xmax - xmin)) + C
                    new_y = int((point.y() - self.__ymin) * canvas_height / (self.__ymax - self.__ymin)) + C / 2

                    # reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.__B_is_rescaled = True
            else:
                for point in self.__B:
                    new_x = int((point.x() - xmin) * canvas_width / (xmax - xmin)) + C
                    new_y = int((point.y() - self.__ymin) * canvas_width / (self.__ymax - self.__ymin)) + C / 2

                    # reposition coordinates accordingly
                    point.setX(new_x)
                    point.setY(new_y)
                self.__B_is_rescaled = True

    def paintEvent(self, e: QPaintEvent):

        # create graphic object
        qp = QPainter(self)

        # start draw
        qp.begin(self)

        # set attributes for line
        qp.setPen(Qt.GlobalColor.black)

        # draw L
        qp.drawPolyline(self.__L)

        # set attributes for barrier
        qp.setPen(Qt.GlobalColor.blue)

        # draw B
        qp.drawPolyline(self.__B)

        # set attributes for displaced line
        qp.setPen(Qt.GlobalColor.red)

        # draw LD
        qp.drawPolyline(self.__LD)

        # end draw
        qp.end()

    # return line
    def getL(self):
        return self.__L

    # return barrier
    def getB(self):
        return self.__B

    # set displaced line
    def setLD(self, LD_):
        self.__LD = LD_

    # set source to load line or barrier
    def setSource(self, status):
        self.__add_L = status

    # clear Canvas
    def clearAll(self):
        self.__L.clear()
        self.__B.clear()
        self.__LD.clear()
        self.__min_max = []
        self.__xmin = inf
        self.__xmax = -inf
        self.__ymin = inf
        self.__ymax = -inf
