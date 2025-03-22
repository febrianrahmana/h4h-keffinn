import sys
from PySide6 import QtCore, QtWidgets, QtGui
from welcomescreen import Ui_Dialog as WelcomeScreen
from welcomescreen2 import Ui_Dialog as WelcomeScreen2
from test import Ui_Dialog as TestScreen

class SplashScreenApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(1440, 1024)
        
        self.setWindowFlags(
            QtCore.Qt.WindowType.Window |
            QtCore.Qt.WindowType.CustomizeWindowHint |
            QtCore.Qt.WindowType.WindowTitleHint |
            QtCore.Qt.WindowType.WindowCloseButtonHint
        )
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setFixedSize(1440, 1024)
        main_layout.addWidget(self.stacked_widget)

        self.splash_screen = QtWidgets.QDialog()
        self.splash_screen.setFixedSize(1440, 1024)
        self.ui_splash = WelcomeScreen()
        self.ui_splash.setupUi(self.splash_screen)
        self.stacked_widget.addWidget(self.splash_screen)

        self.main_screen = QtWidgets.QDialog()
        self.main_screen.setFixedSize(1440, 1024)
        self.ui_main = WelcomeScreen2()
        self.ui_main.setupUi(self.main_screen)
        self.stacked_widget.addWidget(self.main_screen)

        self.test_screen = QtWidgets.QDialog()
        self.test_screen.setFixedSize(1440, 1024)
        self.ui_test = TestScreen()
        self.ui_test.setupUi(self.test_screen)
        self.stacked_widget.addWidget(self.test_screen)

        self.stacked_widget.setCurrentIndex(0)
        self.show()
        QtCore.QTimer.singleShot(3000, self.show_main_window)

        self.ui_main.pushButton.clicked.connect(self.show_test_screen)

    def show_main_window(self):
        self.stacked_widget.setCurrentIndex(1)
        self.ui_main.startAnimations() 

    def show_test_screen(self):
        self.stacked_widget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = SplashScreenApp()
    desktop = app.primaryScreen().availableGeometry()
    window.move((desktop.width() - window.width()) // 2, (desktop.height() - window.height()) // 2)
    
    sys.exit(app.exec())