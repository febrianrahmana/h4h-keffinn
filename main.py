# main.py
import sys
from PySide6 import QtCore, QtWidgets
from welcomescreen import Ui_Dialog as WelcomeScreen
from welcomescreen2 import Ui_Dialog as WelcomeScreen2
from test import Ui_Dialog as TestScreen

class SplashScreenApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Buat QStackedWidget sebagai wadah untuk beberapa halaman
        self.stacked_widget = QtWidgets.QStackedWidget()

        # Tambahkan splash screen ke QStackedWidget
        self.splash_screen = QtWidgets.QDialog()
        self.ui_splash = WelcomeScreen()
        self.ui_splash.setupUi(self.splash_screen)
        self.stacked_widget.addWidget(self.splash_screen)

        # Tambahkan main screen (WelcomeScreen2) ke QStackedWidget
        self.main_screen = QtWidgets.QDialog()
        self.ui_main = WelcomeScreen2()
        self.ui_main.setupUi(self.main_screen)
        self.stacked_widget.addWidget(self.main_screen)

        # Tambahkan test screen ke QStackedWidget
        self.test_screen = QtWidgets.QDialog()
        self.ui_test = TestScreen()
        self.ui_test.setupUi(self.test_screen)
        self.stacked_widget.addWidget(self.test_screen)

        # Tampilkan splash screen pertama kali
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.showMaximized()  # Maximize window saat di-run

        # Set timer untuk beralih ke main screen setelah 3 detik
        QtCore.QTimer.singleShot(3000, self.show_main_window)

        # Hubungkan tombol di main screen ke test screen
        self.ui_main.pushButton.clicked.connect(self.show_test_screen)

    def show_main_window(self):
        # Beralih ke main screen (WelcomeScreen2)
        self.stacked_widget.setCurrentIndex(1)
        self.ui_main.startAnimations()  # Jalankan animasi setelah beralih ke main screen

    def show_test_screen(self):
        # Beralih ke test screen
        self.stacked_widget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SplashScreenApp()
    sys.exit(app.exec())