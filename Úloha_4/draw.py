from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import csv

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # line, barrier and displaced line
        self.__add_L = True
        self.__L = []
        self.__B = []
        self.__LD = []
        self.__min_max = []

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

        # initialize lists of coordinates
        x_list = []
        y_list = []

        # read file
        with open(path, "r", encoding='utf-8-sig') as f:
            for row in csv.reader(f, delimiter='\t'):
                # extract coordinates and convert them to float
                x_list.append(float(row[0]))
                y_list.append(float(row[1]))

        # set min and max x, y coordinates
        if self.__min_max == []:
            self.__min_max = [min(x_list), min(y_list), max(x_list), max(y_list)]

        width = width - 100
        height = height - 100

        # rescale data to fit the window of application
        for i in range(len(x_list)):
            x = int(((x_list[i] - self.__min_max[0]) / (self.__min_max[2] - self.__min_max[0]) * width)) + 50
            y = int((height - (y_list[i] - self.__min_max[1]) / (self.__min_max[3] - self.__min_max[1]) * (height))) + 50
            p = QPointF(x, y)

            # add point to L
            if self.__add_L:
                self.__L.append(p)

            # add point to B
            else:
                self.__B.append(p)

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
