from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class Algorithms:
    def __init__(self):
        pass

    def RayCrossing(self, q, pol):
        # počet průsečíků (k), number of vertices (n)
        k = 0
        n = len(pol)

        # process all vertices
        for i in range(n):
            # reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            # modulo (%n), abychom nepřekročili index, poslední bod bude zase ten první
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()

            # suitable segment - protnutý horizontálním paprskem, oba konce v jiných polorovinách nebo...
            if yi1r > 0 and yir <= 0 or yir > 0 and yi1r <= 0:
                # compute intersection
                xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)

                # increment amount of intersections
                if xm > 0:
                    k += 1

        # point is inside
        if k % 2 == 1:
            return 1
        return 0