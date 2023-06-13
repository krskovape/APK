from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms
from settings import InputDialog


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuElement = QtWidgets.QMenu(parent=self.menubar)
        self.menuElement.setObjectName("menuElement")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
        self.menuOptions = QtWidgets.QMenu(parent=self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionDisplace_1_element = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/displace.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionDisplace_1_element.setIcon(icon)
        self.actionDisplace_1_element.setObjectName("actionDisplace_1_element")
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon1)
        self.actionClear.setObjectName("actionClear")
        self.actionSettings = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionSettings.setIcon(icon2)
        self.actionSettings.setObjectName("actionSettings")
        self.actionElement = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/element.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionElement.setIcon(icon3)
        self.actionElement.setObjectName("actionElement")
        self.actionBarrier = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/barrier.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionBarrier.setIcon(icon5)
        self.actionBarrier.setObjectName("actionBarrier")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon6)
        self.actionExit.setObjectName("actionExit")
        self.menuElement.addAction(self.actionElement)
        self.menuElement.addAction(self.actionBarrier)
        self.menuSimplify.addAction(self.actionDisplace_1_element)
        self.menuSimplify.addSeparator()
        self.menuSimplify.addAction(self.actionClear)
        self.menuOptions.addAction(self.actionSettings)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionExit)
        self.menubar.addAction(self.menuElement.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.toolBar.addAction(self.actionElement)
        self.toolBar.addAction(self.actionBarrier)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDisplace_1_element)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        # connect signals to slots
        self.actionDisplace_1_element.triggered.connect(self.displaceClick)
        self.actionElement.triggered.connect(self.drawLineClick)
        self.actionBarrier.triggered.connect(self.drawBarrierClick)
        self.actionClear.triggered.connect(self.clearClick)
        self.actionSettings.triggered.connect(self.runSettings)
        self.actionExit.triggered.connect(sys.exit)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Energy splines"))
        self.menuElement.setTitle(_translate("MainForm", "Input"))
        self.menuSimplify.setTitle(_translate("MainForm", "Simplify"))
        self.menuOptions.setTitle(_translate("MainForm", "Options"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionDisplace_1_element.setText(_translate("MainForm", "Displace 1 element"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionSettings.setText(_translate("MainForm", "Settings"))
        self.actionElement.setText(_translate("MainForm", "Element"))
        self.actionElement.setToolTip(_translate("MainForm", "Load element"))
        self.actionBarrier.setText(_translate("MainForm", "Barrier"))
        self.actionBarrier.setToolTip(_translate("MainForm", "Load barrier"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionExit.setToolTip(_translate("MainForm", "Exit application"))

    # initialize parameters
    def __init__(self):
        self.__dmin = 100
        self.__alpha = 1
        self.__beta = 1000
        self.__gamma = 10
        self.__lam = 10
        self.__iters = 50

    # set properties
    def runSettings(self):
        # call dialog window, set energy spline properties
        dialog = InputDialog(self.__dmin, self.__alpha, self.__beta, self.__gamma, self.__lam, self.__iters)

        # on signal accepted
        if dialog.exec():
            # get input values
            dmin, alpha, beta, gamma, lam, iters = dialog.getInputs()

            # convert input values to integer and set it as energy spline properties
            self.__dmin = int(dmin)
            self.__alpha = float(alpha)
            self.__beta = float(beta)
            self.__gamma = float(gamma)
            self.__lam = float(lam)
            self.__iters = int(iters)

        else:
            return

    # load points from input file
    def openFile(self):
        width = self.Canvas.frameSize().width()
        height = self.Canvas.frameSize().height()
        self.Canvas.loadData(width, height)

    # compute displaced line
    def displaceClick(self):
        # get polyline and barrier
        L = self.Canvas.getL()
        B = self.Canvas.getB()

        # run displacement
        a = Algorithms()
        LD = a.minEnergySpline(L, B, self.__alpha, self.__beta, self.__gamma, self.__lam, self.__dmin, self.__iters)

        # set results
        self.Canvas.setLD(LD)

        # repaint
        self.Canvas.repaint()

    # load line data
    def drawLineClick(self):
        self.Canvas.setSource(True)
        self.openFile()

    # load barrier data
    def drawBarrierClick(self):
        self.Canvas.setSource(False)
        self.openFile()

    # clear Canvas
    def clearClick(self):
        self.Canvas.clearAll()
        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
