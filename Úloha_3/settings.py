from PyQt6.QtWidgets import *

class InputDialog(QDialog):
    def __init__(self, min, max, st):
        super().__init__(parent=None)

        # set window title
        self.setWindowTitle("Contour lines properties")

        # initialize properties
        self.__cmin = QLineEdit(self)
        self.__cmax = QLineEdit(self)
        self.__step = QLineEdit(self)

        # set text of input lines
        self.__cmin.setText(str(min))
        self.__cmax.setText(str(max))
        self.__step.setText(str(st))

        # create button box with Ok and Cancel button
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        # create layout
        layout = QFormLayout(self)
        layout.addRow("Min", self.__cmin)
        layout.addRow("Max", self.__cmax)
        layout.addRow("Step", self.__step)
        layout.addWidget(buttonBox)

        # accept or reject changed parameters
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # return set properties
    def getInputs(self):
        return (self.__cmin.text(), self.__cmax.text(), self.__step.text())