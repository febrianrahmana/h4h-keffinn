import sys, platform
from PySide6 import QtCore, QtWidgets, QtGui
from welcomescreen import Ui_Dialog as WelcomeScreen
from welcomescreen2 import Ui_Dialog as WelcomeScreen2
from test import Ui_Dialog as TestScreen
from EyetrackingThread import EyetrackingThread
from SpeechThread import SpeechThread
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction

def is_dark_mode() -> bool:
    system = platform.system()

    if system == "Windows":
        # Windows: Check the registry for dark mode settings
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 means dark mode, 1 means light mode
        except Exception:
            return False  # Fallback if registry access fails

    elif system == "Darwin":
        # macOS: Use AppleScript to check the appearance
        try:
            import subprocess
            script = 'tell application "System Events" to tell appearance preferences to get dark mode'
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            return result.stdout.strip() == "true"
        except Exception:
            return False  # Fallback if AppleScript fails

    elif system == "Linux":
        # Linux: Check GTK or GNOME settings (this may vary depending on the desktop environment)
        try:
            import subprocess
            result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"], capture_output=True, text=True)
            theme = result.stdout.strip().lower()
            return "dark" in theme  # Assumes dark themes contain "dark" in their name
        except Exception:
            return False  # Fallback if gsettings fails

    else:
        # Unsupported platform
        return False

class SplashScreenApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Eye Hear U")
        
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
        
    def bring_to_top(self):
        self.show()
        self.raise_()
        self.activateWindow()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = SplashScreenApp()
    desktop = app.primaryScreen().availableGeometry()
    window.move((desktop.width() - window.width()) // 2, (desktop.height() - window.height()) // 2)
    window.show()
    
    
    # Tray Icon
    tray_icon = QSystemTrayIcon()
    
    # Check if the system is in dark mode
    if is_dark_mode():
        tray_icon.setIcon(QIcon("./static/dark_logo.png"))
    else:
        tray_icon.setIcon(QIcon("./static/light_logo.png"))
    
    # Menu in system tray
    menu = QMenu()
    
    action_show = QAction("Show", menu)
    action_hide = QAction("Hide", menu)
    action_quit = QAction("Quit", menu)
    
    action_show.triggered.connect(lambda: window.bring_to_top())
    action_hide.triggered.connect(lambda: window.hide())
    action_quit.triggered.connect(app.quit)
    
    menu.addAction(action_show)
    menu.addAction(action_hide)
    menu.addSeparator()
    menu.addAction(action_quit)
    
    tray_icon.setContextMenu(menu)
    
    tray_icon.activated.connect(lambda reason: menu.popup(QtGui.QCursor.pos()) if reason == QSystemTrayIcon.Trigger else None)
    
    tray_icon.show()
    
    sys.exit(app.exec())