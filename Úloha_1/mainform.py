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
        self.Toolbar = Draw(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizePolicy)
        self.Toolbar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Toolbar.setObjectName("Toolbar")
        self.label = QtWidgets.QLabel(parent=self.Toolbar)
        self.label.setGeometry(QtCore.QRect(140, 5, 81, 20))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(parent=self.Toolbar)
        self.comboBox.setGeometry(QtCore.QRect(230, 0, 150, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.buttonInputFile = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonInputFile.setGeometry(QtCore.QRect(10, 0, 30, 30))
        self.buttonInputFile.setStyleSheet("border-image: url(icons/open_file.png);")
        self.buttonInputFile.setText("")
        self.buttonInputFile.setObjectName("buttonInputFile")
        self.buttonAnalyze = QtWidgets.QPushButton(parent=self.Toolbar)
        self.buttonAnalyze.setGeometry(QtCore.QRect(60, 0, 30, 30))
        self.buttonAnalyze.setStyleSheet("border-image: url(icons/polygon.png);")
        self.buttonAnalyze.setText("")
        self.buttonAnalyze.setObjectName("buttonAnalyze")
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
        self.menuFile.addAction(self.actionOpen)
        self.menuAnalyze.addAction(self.actionPointInPolygon)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAnalyze.menuAction())

        self.buttonInputFile.clicked.connect(self.openFile)
        self.buttonAnalyze.clicked.connect(self.analyze)
        self.actionPointInPolygon.triggered.connect(self.analyze)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Point in polygon position"))
        self.label.setText(_translate("MainForm", "Algorithm:"))
        self.comboBox.setItemText(0, _translate("MainForm", "Winding Number"))
        self.comboBox.setItemText(1, _translate("MainForm", "Ray Crossing"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionPointInPolygon.setText(_translate("MainForm", "PointInPolygon"))

    def openFile(self):
        width = self.Canvas.frameSize().width()
        height = self.Canvas.frameSize().height()
        self.Canvas.loadFile(width, height)

    def analyze(self):
        q = self.Canvas.getPoint()
        polygons = self.Canvas.getPolygons()

        # analyze position
        a = Algorithms()

        self.Canvas.__pol_index = [None] * len(polygons)

        for index, pol in enumerate(polygons):
            #if self.comboBox.currentIndex() == 1:
                #result = a.RayCrossing(q, pol)
                #self.Canvas.__polygon_index[index] = result
            result = a.RayCrossing(q, pol)
            #self.Canvas.__pol_index[index] = result
            self.Canvas.__pol_index.append(result)

        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
