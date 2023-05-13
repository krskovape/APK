from PyQt6.QtWidgets import *

class InputDialog(QDialog):
    def __init__(self, i_dmin, i_aplha, i_beta, i_gamma, i_lam, i_iters):
        super().__init__(parent=None)

        # set window title
        self.setWindowTitle("Parameters of energy splines")

        # initialize properties
        self.__dmin = QLineEdit(self)
        self.__alpha = QLineEdit(self)
        self.__beta = QLineEdit(self)
        self.__gamma = QLineEdit(self)
        self.__lam = QLineEdit(self)
        self.__iters = QLineEdit(self)

        # set text of input lines
        self.__dmin.setText(str(i_dmin))
        self.__alpha.setText(str(i_aplha))
        self.__beta.setText(str(i_beta))
        self.__gamma.setText(str(i_gamma))
        self.__lam.setText(str(i_lam))
        self.__iters.setText(str(i_iters))

        # create button box with Ok and Cancel button
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        # create layout
        layout = QFormLayout(self)
        layout.addRow("Minimum distance", self.__dmin)
        layout.addRow("Alpha", self.__alpha)
        layout.addRow("Beta", self.__beta)
        layout.addRow("Gamma", self.__gamma)
        layout.addRow("Lambda", self.__lam)
        layout.addRow("Number of iterations", self.__iters)
        layout.addWidget(buttonBox)

        # accept or reject changed parameters
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # return set properties
    def getInputs(self):
        return (self.__dmin.text(), self.__alpha.text(), self.__beta.text(), self.__gamma.text(), self.__lam.text(), self.__iters.text())