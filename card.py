# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(454, 355)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 30, 376, 68))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"    border: 2px solid #9266CC;\n"
"    font-family: 'Nunito', sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QPushButton[checked=\"true\"] {\n"
"    background-color: #A3D8FF; /* Change color when checked */\n"
"    border: 2px solid #4A8CB0;  /* Optional: border color when checked */\n"
"}\n"
"")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(40, 100, 376, 68))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"    border: 2px solid #9266CC;\n"
"    font-family: 'Nunito', sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QPushButton[checked=\"true\"] {\n"
"    background-color: #A3D8FF; /* Change color when checked */\n"
"    border: 2px solid #4A8CB0;  /* Optional: border color when checked */\n"
"}\n"
"")
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(40, 170, 376, 68))
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"    border: 2px solid #9266CC;\n"
"    font-family: 'Nunito', sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QPushButton[checked=\"true\"] {\n"
"    background-color: #A3D8FF; /* Change color when checked */\n"
"    border: 2px solid #4A8CB0;  /* Optional: border color when checked */\n"
"}\n"
"")
        self.pushButton_4 = QPushButton(Dialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(40, 240, 376, 68))
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border-radius: 10px;\n"
"    border: 2px solid #9266CC;\n"
"    font-family: 'Nunito', sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QPushButton[checked=\"true\"] {\n"
"    background-color: #A3D8FF; /* Change color when checked */\n"
"    border: 2px solid #4A8CB0;  /* Optional: border color when checked */\n"
"}\n"
"")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Tentang EYE HEAR U", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Microphone", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"EYE Tracking", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Settings", None))
    # retranslateUi

