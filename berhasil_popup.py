from PySide6 import QtCore, QtGui, QtWidgets
import sys
from PySide6.QtGui import QFont

class BerhasilDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Connect the button to close the dialog
        self.ui.pushButton.clicked.connect(self.accept)
        
        # Set window flags to make it stay on top
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        
    @staticmethod
    def show_dialog(parent=None):
        dialog = BerhasilDialog(parent)
        dialog.exec()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 400)
        Dialog.setFixedSize(800, 400)
        Dialog.setStyleSheet("background-color:rgb(141, 177, 196)")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 50, 600, 131))  
        font = QtGui.QFont()
        font.setFamily("Nunito")
        font.setPointSize(42) 
        font.setBold(True)
        font.setWeight(QFont.Thin)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(370, 160, 71, 71))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-image:url(:/newPrefix/berhasil.png)")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/newPrefix/berhasil.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(240, 260, 321, 91))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 20px;\n"
"    color: #4A8CB0;\n"
"    font-size: 25px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(240, 240, 240);\n"
"    color: rgb(60, 120, 160);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(220, 220, 220);\n"
"    color: rgb(50, 100, 140);\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kalibrasi"))
        # Make sure there's no unwanted line breaks in the HTML
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">Kalibrasi Berhasil</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Kembali"))

import icons_rc

if __name__ == "__main__":
    # Demo code when run directly
    app = QtWidgets.QApplication(sys.argv)
    dialog = BerhasilDialog()
    dialog.show()
    sys.exit(app.exec())