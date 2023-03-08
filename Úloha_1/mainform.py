from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(922, 695)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Toolbar = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizePolicy)
        self.Toolbar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Toolbar.setObjectName("Toolbar")
        self.label = QtWidgets.QLabel(parent=self.Toolbar)
        self.label.setGeometry(QtCore.QRect(220, 5, 71, 20))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(parent=self.Toolbar)
        self.comboBox.setGeometry(QtCore.QRect(290, 0, 120, 30))
        self.comboBox.setToolTip("Switch algorithm")
        self.comboBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.buttonInputFile = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonInputFile.setGeometry(QtCore.QRect(0, 0, 30, 30))
        self.buttonInputFile.setToolTip("Insert file")
        self.buttonInputFile.setStyleSheet("QPushButton {border-image: url(icons/open_file.png);}")
        self.buttonInputFile.setText("")
        self.buttonInputFile.setObjectName("buttonInputFile")
        self.buttonAnalyze = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonAnalyze.setGeometry(QtCore.QRect(45, 0, 30, 30))
        self.buttonAnalyze.setToolTip("Analyze point and polygon position")
        self.buttonAnalyze.setStyleSheet("QPushButton {border-image: url(icons/polygon.png);}")
        self.buttonAnalyze.setText("")
        self.buttonAnalyze.setObjectName("buttonAnalyze")
        self.buttonClear = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonClear.setGeometry(QtCore.QRect(90, 0, 30, 30))
        self.buttonClear.setToolTip("Clear")
        self.buttonClear.setStyleSheet("QPushButton {border-image: url(icons/clear.png);}")
        self.buttonClear.setText("")
        self.buttonClear.setObjectName("buttonClear")
        self.buttonRepaint = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonRepaint.setGeometry(QtCore.QRect(135, 0, 30, 30))
        self.buttonRepaint.setToolTip("Fit to display")
        self.buttonRepaint.setText("")
        self.buttonRepaint.setObjectName("buttonRepaint")
        self.verticalLayout.addWidget(self.Toolbar)
        self.Canvas = Draw(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.verticalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=MainForm)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 922, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(parent=self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menuBar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        self.menuEdit = QtWidgets.QMenu(parent=self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        MainForm.setMenuBar(self.menuBar)
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionPointInPolygon = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/polygon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPointInPolygon.setIcon(icon1)
        self.actionPointInPolygon.setObjectName("actionPointInPolygon")
        self.actionFitToDisplay = QtGui.QAction(parent=MainForm)
        self.actionFitToDisplay.setObjectName("actionFitToDisplay")
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon2)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon3)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuAnalyze.addAction(self.actionPointInPolygon)
        self.menuEdit.addAction(self.actionFitToDisplay)
        self.menuEdit.addAction(self.actionClear)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAnalyze.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.actionOpen.triggered.connect(self.openFile)
        self.actionExit.triggered.connect(sys.exit)
        self.actionPointInPolygon.triggered.connect(self.analyze)
        self.actionFitToDisplay.triggered.connect(self.fitToDisplay)
        self.actionClear.triggered.connect(self.clearCanvas)
        self.buttonInputFile.clicked.connect(self.openFile)
        self.buttonAnalyze.clicked.connect(self.analyze)
        self.buttonClear.clicked.connect(self.clearCanvas)
        self.buttonRepaint.clicked.connect(self.fitToDisplay)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Point and polygon location"))
        self.label.setText(_translate("MainForm", "Algorithm:"))
        self.comboBox.setItemText(0, _translate("MainForm", "Winding Number"))
        self.comboBox.setItemText(1, _translate("MainForm", "Ray Crossing"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.menuEdit.setTitle(_translate("MainForm", "Edit"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionPointInPolygon.setText(_translate("MainForm", "Point In Polygon"))
        self.actionFitToDisplay.setText(_translate("MainForm", "Fit To Display"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionExit.setText(_translate("MainForm", "Exit"))

    def openFile(self):
        width = self.Canvas.frameSize().width()
        height = self.Canvas.frameSize().height()
        self.Canvas.loadData()
        self.Canvas.rescaleData(width, height)

    def analyze(self):
        q = self.Canvas.getPoint()
        polygons = self.Canvas.getPolygons()

        # analyze position
        a = Algorithms()

        for index, pol in enumerate(polygons):
            if self.comboBox.currentIndex() == 0:
                result = a.windingNumber(q, pol)
                self.Canvas.setResult(result)
            if self.comboBox.currentIndex() == 1:
                result = a.rayCrossing(q, pol)
                self.Canvas.setResult(result)

        self.Canvas.repaint()

    def clearCanvas(self):
        self.Canvas.clearPol()

    def fitToDisplay(self):
        width = self.Canvas.frameSize().width()
        height = self.Canvas.frameSize().height()
        self.Canvas.rescaleData(width, height)
        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
