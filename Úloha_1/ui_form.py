# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

from draw import Draw
import Icons_rc

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(922, 695)
        MainForm.setStyleSheet(u"#buttonInputFile {\n"
"background-color: transparent;\n"
"border-image: url(:/images/icons/open_file.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#buttonInputFile:pressed\n"
"{\n"
"   border-image: url(:/images/icons/open_file.png);\n"
"}")
        self.actionOpen = QAction(MainForm)
        self.actionOpen.setObjectName(u"actionOpen")
        icon = QIcon()
        icon.addFile(u":/images/icons/open_file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionPointInPolygon = QAction(MainForm)
        self.actionPointInPolygon.setObjectName(u"actionPointInPolygon")
        icon1 = QIcon()
        icon1.addFile(u":/images/icons/polygon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPointInPolygon.setIcon(icon1)
        self.centralwidget = QWidget(MainForm)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Toolbar = Draw(self.centralwidget)
        self.Toolbar.setObjectName(u"Toolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizePolicy)
        self.Toolbar.setMaximumSize(QSize(16777215, 30))
        self.label = QLabel(self.Toolbar)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 5, 81, 20))
        self.comboBox = QComboBox(self.Toolbar)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(230, 0, 150, 30))
        self.buttonInputFile = QPushButton(self.Toolbar)
        self.buttonInputFile.setObjectName(u"buttonInputFile")
        self.buttonInputFile.setGeometry(QRect(10, 0, 30, 30))
        self.buttonInputFile.setStyleSheet(u"border-image: url(:/images/icons/open_file.png);\n"
"\n"
"")
        self.buttonAnalyze = QPushButton(self.Toolbar)
        self.buttonAnalyze.setObjectName(u"buttonAnalyze")
        self.buttonAnalyze.setGeometry(QRect(60, 0, 30, 30))
        self.buttonAnalyze.setStyleSheet(u"border-image: url(:/images/icons/polygon.png);")

        self.verticalLayout.addWidget(self.Toolbar)

        self.Canvas = Draw(self.centralwidget)
        self.Canvas.setObjectName(u"Canvas")
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.Canvas)

        MainForm.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainForm)
        self.statusbar.setObjectName(u"statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainForm)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 922, 26))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAnalyze = QMenu(self.menuBar)
        self.menuAnalyze.setObjectName(u"menuAnalyze")
        MainForm.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAnalyze.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuAnalyze.addAction(self.actionPointInPolygon)

        self.retranslateUi(MainForm)

        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"MainForm", None))
        self.actionOpen.setText(QCoreApplication.translate("MainForm", u"Open", None))
        self.actionPointInPolygon.setText(QCoreApplication.translate("MainForm", u"PointInPolygon", None))
        self.label.setText(QCoreApplication.translate("MainForm", u"Algorithm:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainForm", u"Winding Number", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainForm", u"Ray Crossing", None))

        self.buttonInputFile.setText("")
        self.buttonAnalyze.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainForm", u"File", None))
        self.menuAnalyze.setTitle(QCoreApplication.translate("MainForm", u"Analyze", None))
    # retranslateUi

