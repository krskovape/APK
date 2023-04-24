from QPoint3DF import *

class Edge:
    def __init__(self, start: QPoint3DF, end: QPoint3DF):
        self.__start = start
        self.__end = end

    # return start point
    def getStart(self):
        return self.__start

    # return end point
    def getEnd(self):
        return self.__end

    # create new edge with an opposite orientation
    def switchOrientation(self):
        return Edge(self.__end, self.__start)

    # compare two edges
    def __eq__(self, other):
        return (self.__start == other.__start) and (self.__end == other.__end)