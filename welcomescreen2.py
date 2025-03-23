# welcomescreen2.py
from PySide6 import QtCore, QtGui, QtWidgets
import keffinn_rc
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1440, 1024)
        
        Dialog.setFixedSize(1440, 1024)
        
        Dialog.setWindowFlags(
            QtCore.Qt.WindowType.Window |
            QtCore.Qt.WindowType.CustomizeWindowHint |
            QtCore.Qt.WindowType.WindowTitleHint |
            QtCore.Qt.WindowType.WindowCloseButtonHint
        )

        font_id = QtGui.QFontDatabase.addApplicationFont("src/Nunito-Bold.otf")
        if font_id != -1:
            font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                self.font_family = font_families[0]
            else:
                self.font_family = "MS Shell Dlg 2"
        else:
            print("Font tidak berhasil dimuat. Pastikan file Nunito-Bold.otf ada di folder src.")
            self.font_family = "MS Shell Dlg 2"

        # Background widget
        self.bgwidget = QtWidgets.QWidget(parent=Dialog)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 1440, 1024))
        self.bgwidget.setStyleSheet("QWidget#bgwidget{\n"
"background-image: url(:/img/background.png)\n"
"};")
        self.bgwidget.setObjectName("bgwidget")

        icon_width = 291
        icon_x = (1440 - icon_width) // 2
        self.icon = QtWidgets.QLabel(parent=self.bgwidget)
        self.icon.setGeometry(QtCore.QRect(icon_x, 100, icon_width, 191))
        self.icon.setStyleSheet("background-image: url(:/img/logo_putih.png);")
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap(":/img/logo_putih.png"))
        self.icon.setScaledContents(True)
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.icon.setObjectName("icon")

        self.footer = QtWidgets.QLabel(parent=self.bgwidget)
        self.footer.setGeometry(QtCore.QRect(0, 1024, 1441, 591))
        self.footer.setStyleSheet("background-color: rgb(74, 140, 176);")
        self.footer.setText("")
        self.footer.setObjectName("footer")

        label_width = 1161
        label_x = (1440 - label_width) // 2
        self.label = QtWidgets.QLabel(parent=self.bgwidget)
        self.label.setGeometry(QtCore.QRect(label_x, 1024, label_width, 131))
        self.label.setStyleSheet("text-color:white;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        button_width = 611
        button_x = (1440 - button_width) // 2
        self.pushButton = QtWidgets.QPushButton(parent=self.bgwidget)
        self.pushButton.setGeometry(QtCore.QRect(button_x, 1024, button_width, 101))

        self.pushButton.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: rgb(74, 140, 176);
                font-family: '{self.font_family}';
                font-size: 22pt;
                font-weight: bold;
                border-radius: 40px;
                transition: background-color 0.3s;
            }}

            QPushButton:hover {{
                background-color: rgb(240, 240, 240);
                color: rgb(60, 120, 160);
                border: 2px solid rgb(74, 140, 176);
            }}

            QPushButton:pressed {{
                background-color: rgb(220, 220, 220);
                color: rgb(50, 100, 140);
                border: 3px solid rgb(74, 140, 176);
            }}
        """)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def startAnimations(self):
        # footer
        self.footerAnimation = QtCore.QPropertyAnimation(self.footer, b"geometry")
        self.footerAnimation.setDuration(800)
        self.footerAnimation.setStartValue(QtCore.QRect(0, 1024, 1441, 591))
        self.footerAnimation.setEndValue(QtCore.QRect(0, 430, 1441, 591))
        self.footerAnimation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuint)

        # label - maintain center position in animation
        label_width = 1161
        label_x = (1440 - label_width) // 2
        self.labelAnimation = QtCore.QPropertyAnimation(self.label, b"geometry")
        self.labelAnimation.setDuration(800)
        self.labelAnimation.setStartValue(QtCore.QRect(label_x, 1024, label_width, 131))
        self.labelAnimation.setEndValue(QtCore.QRect(label_x, 520, label_width, 131))
        self.labelAnimation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuint)

        # button - maintain center position in animation
        button_width = 611
        button_x = (1440 - button_width) // 2
        self.buttonAnimation = QtCore.QPropertyAnimation(self.pushButton, b"geometry")
        self.buttonAnimation.setDuration(800)
        self.buttonAnimation.setStartValue(QtCore.QRect(button_x, 1024, button_width, 101))
        self.buttonAnimation.setEndValue(QtCore.QRect(button_x, 680, button_width, 101))
        self.buttonAnimation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuint)

        self.animationGroup = QtCore.QParallelAnimationGroup()

        self.animationGroup.addAnimation(self.footerAnimation)

        self.labelDelay = QtCore.QSequentialAnimationGroup()
        self.labelDelay.addPause(100)
        self.labelDelay.addAnimation(self.labelAnimation)
        self.animationGroup.addAnimation(self.labelDelay)

        self.buttonDelay = QtCore.QSequentialAnimationGroup()
        self.buttonDelay.addPause(200)
        self.buttonDelay.addAnimation(self.buttonAnimation)
        self.animationGroup.addAnimation(self.buttonDelay)

        self.animationGroup.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", f"""<html><head/><body>
        <p align=\"center\"><span style=\" font-family:'{self.font_family}'; font-size:22pt; font-weight:600; color:#ffffff;\">Kendalikan perangkatmu dengan gerakan mata dan suara untuk</span></p>
        <p align=\"center\"><span style=\" font-family:'{self.font_family}'; font-size:22pt; font-weight:600; color:#ffffff;\">pengalaman digital yang lebih mudah dan inklusif.</span></p>
        </body></html>"""))
        self.pushButton.setText(_translate("Dialog", "Mulai Kalibrasi"))


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     ui.startAnimations() 
#     sys.exit(app.exec())