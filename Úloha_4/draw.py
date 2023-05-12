from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import csv

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Query point and polygon
        self.__add_L = True
        self.__L = []
        self.__B = []
        self.__LD = []

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
        with open(path, "r") as f:
            for row in csv.reader(f, delimiter='\t'):
                # extract coordinates and convert them to float
                x_list.append(float(row[0]))
                y_list.append(float(row[1]))

        # get min and max x, y coordinates
        min_max = [min(x_list), min(y_list), max(x_list), max(y_list)]

        # rescale data to fit the window of application
        for i in range(len(x_list)):
            x = int(((x_list[i] - min_max[0]) / (min_max[2] - min_max[0]) * width))
            y = int((height - (y_list[i] - min_max[1]) / (min_max[3] - min_max[1]) * (height)))
            p = QPointF(x, y)

            # add point to L
            if self.__add_L:
                self.__L.append(p)

            # add point to B
            else:
                self.__B.append(p)

    def mousePressEvent(self, e: QMouseEvent):
        # Left mouse button click
        x = e.position().x()
        y = e.position().y()

        # Create new point
        p = QPointF(x, y)

        # Add point to L
        if self.__add_L:
            self.__L.append(p)

        # Add point to B
        else:
            self.__B.append(p)

        # Repaint screen
        self.repaint()


    def paintEvent(self, e: QPaintEvent):

        # Create graphic object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set attributes
        qp.setPen(Qt.GlobalColor.black)

        # Draw L
        qp.drawPolyline(self.__L)

        # Set attributes
        qp.setPen(Qt.GlobalColor.blue)

        # Draw B
        qp.drawPolyline(self.__B)

        # Set attributes
        qp.setPen(Qt.GlobalColor.red)

        # Draw LD
        qp.drawPolyline(self.__LD)

        # End draw
        qp.end()

    def getL(self):
        return self.__L


    def getB(self):
        return self.__B


    def setLD(self, LD_):
        self.__LD = LD_


    def setSource(self, status):
        self.__add_L = status

    def clearAll(self):
        self.__L.clear()
        self.__B.clear()
        self.__LD.clear()
