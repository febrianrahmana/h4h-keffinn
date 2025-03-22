from PySide6 import QtCore, QtGui, QtWidgets
import sys
from src import keffinn_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1440, 1024)
        Dialog.setStyleSheet("")
        self.bgwidget = QtWidgets.QWidget(parent=Dialog)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 1440, 1024))
        self.bgwidget.setStyleSheet("QWidget#bgwidget{\n"
"background-image: url(:/img/background.png);\n"
"};")
        self.bgwidget.setObjectName("bgwidget")
        self.label = QtWidgets.QLabel(parent=self.bgwidget)
        self.label.setGeometry(QtCore.QRect(560, 330, 351, 241))
        self.label.setStyleSheet("background-image: url(:/img/logo_putih.png);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/img/logo_putih.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
