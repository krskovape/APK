from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1107, 600)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1107, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClose.setIcon(icon1)
        self.actionClose.setObjectName("actionClose")
        self.actionMinimum_Area_Enclosing_Rectangle = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMinimum_Area_Enclosing_Rectangle.setIcon(icon2)
        self.actionMinimum_Area_Enclosing_Rectangle.setObjectName("actionMinimum_Area_Enclosing_Rectangle")
        self.actionWall_Average = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWall_Average.setIcon(icon3)
        self.actionWall_Average.setObjectName("actionWall_Average")

        self.actionLongest_Edge = QtGui.QAction(parent=MainForm)
        #icon5 = QtGui.QIcon()
        #icon5.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongest_Edge.setIcon(icon3)
        self.actionLongest_Edge.setObjectName("actionLongest_Edge")
        self.actionWeighted_Bisector = QtGui.QAction(parent=MainForm)
        # icon6 = QtGui.QIcon()
        # icon6.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeighted_Bisector.setIcon(icon3)
        self.actionWeighted_Bisector.setObjectName("actionWeighted_Bisector")
        self.actionPrincipal_Component = QtGui.QAction(parent=MainForm)
        # icon7 = QtGui.QIcon()
        # icon7.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPrincipal_Component.setIcon(icon3)
        self.actionPrincipal_Component.setObjectName("actionPrincipal_Component")

        self.actionClear = QtGui.QAction(parent=MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon4)
        self.actionClear.setObjectName("actionClear")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuSimplify.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.menuSimplify.addAction(self.actionWall_Average)
        self.menuSimplify.addAction(self.actionLongest_Edge)
        self.menuSimplify.addAction(self.actionWeighted_Bisector)
        self.menuSimplify.addAction(self.actionPrincipal_Component)
        self.menuSimplify.addSeparator()
        self.menuSimplify.addAction(self.actionClear)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.toolBar.addAction(self.actionWall_Average)
        self.toolBar.addAction(self.actionLongest_Edge)
        self.toolBar.addAction(self.actionWeighted_Bisector)
        self.toolBar.addAction(self.actionPrincipal_Component)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)
        self.label = QtWidgets.QLabel(parent=self.toolBar)
        self.label.setGeometry(QtCore.QRect(280, 6, 120, 20))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(parent=self.toolBar)
        self.comboBox.setGeometry(QtCore.QRect(410, 0, 100, 30))
        self.comboBox.setToolTip("Switch convex hull algorithm")
        self.comboBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        # connect signals to slots
        self.actionOpen.triggered.connect(self.openFile)
        self.actionClose.triggered.connect(sys.exit)
        self.actionMinimum_Area_Enclosing_Rectangle.triggered.connect(self.simplifyMinEnclosingRectangle)
        self.actionWall_Average.triggered.connect(self.simplifyWallAverage)
        self.actionLongest_Edge.triggered.connect(self.simplifyLongestEdge)
        self.actionPrincipal_Component.triggered.connect(self.simplifyPCAClick)
        self.actionClear.triggered.connect(self.clearCanvas)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "BuildingSimplify"))
        self.label.setText(_translate("MainForm", "Convex hull algorithm:"))
        self.comboBox.setItemText(0, _translate("MainForm", "Jarvis Scan"))
        self.comboBox.setItemText(1, _translate("MainForm", "Graham Scan"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuSimplify.setTitle(_translate("MainForm", "Simplify"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionOpen.setToolTip(_translate("MainForm", "Open file"))
        self.actionClose.setText(_translate("MainForm", "Close"))
        self.actionClose.setToolTip(_translate("MainForm", "Close file"))
        self.actionMinimum_Area_Enclosing_Rectangle.setText(_translate("MainForm", "Minimum Area Enclosing Rectangle"))
        self.actionWall_Average.setText(_translate("MainForm", "Wall Average"))
        self.actionLongest_Edge.setText(_translate("MainForm", "Longest Edge"))
        self.actionWeighted_Bisector.setText(_translate("MainForm", "Weighted Bisector"))
        self.actionPrincipal_Component.setText(_translate("MainForm", "Principal Component Analysis"))
        self.actionClear.setText(_translate("MainForm", "Clear"))

    def openFile(self):
        width = self.Canvas.frameSize().width()
        height = self.Canvas.frameSize().height()
        self.Canvas.loadData()
        self.Canvas.rescaleData(width, height)

    def createCH(self, pol):
        a = Algorithms()

        if self.comboBox.currentIndex() == 0:
            ch = a.jarvisScan(pol)
        if self.comboBox.currentIndex() == 1:
            ch = a.grahamScan(pol)

        return ch

    def simplifyMinEnclosingRectangle(self):
        # get polygon
        polygons = self.Canvas.getPolygons()

        a = Algorithms()

        for pol in polygons:

            ch = self.createCH(pol)
            # self.Canvas.setCH(ch)

            er = a.minAreaEnclosingRectangle(pol, ch)
            self.Canvas.setER(er)

        self.Canvas.repaint()

    def simplifyWallAverage(self):
        # get polygon
        polygons = self.Canvas.getPolygons()

        a = Algorithms()

        for pol in polygons:
            ch = self.createCH(pol)
            # self.Canvas.setCH(ch)

            er = a.wallAverage(pol)
            self.Canvas.setER(er)

        self.Canvas.repaint()

    def simplifyLongestEdge(self):
        # get polygon
        pol = self.Canvas.getPolygon()

        a = Algorithms()

        ch = self.createCH(pol)
        #self.Canvas.setCH(ch)

        er = a.longestEdge(pol)
        self.Canvas.setER(er)

        self.Canvas.repaint()

    def simplifyPCAClick(self):
        # get polygon
        pol = self.Canvas.getPolygon()

        a = Algorithms()

        ch = a.jarvisScan(pol)
        self.Canvas.setCH(ch)

        er = a.principalComponent(pol)
        self.Canvas.setER(er)
        #a.principalComponent(pol)

        self.Canvas.repaint()

    def clearCanvas(self):
        self.Canvas.cleanCanvas()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
