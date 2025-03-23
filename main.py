import sys, platform
from PySide6 import QtCore, QtWidgets, QtGui
from welcomescreen import Ui_Dialog as WelcomeScreen
from welcomescreen2 import Ui_Dialog as WelcomeScreen2
from about_keffinn import Ui_Dialog as AboutScreen
from card import Ui_Dialog as CardDialog
from test import Ui_Dialog as TestScreen
from EyetrackingThread import EyetrackingThread
from SpeechThread import SpeechThread
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from berhasil_popup import BerhasilDialog

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
        self.gaze_estimator: EyetrackingThread = EyetrackingThread()
        self.speech_recognition: SpeechThread = SpeechThread()
        self.tray_menu = None

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

        # Settings should be before about screen

        self.about_screen = QtWidgets.QDialog()
        self.about_screen.setFixedSize(1440, 1024)
        self.ui_about = AboutScreen()
        self.ui_about.setupUi(self.about_screen)
        self.stacked_widget.addWidget(self.about_screen)

        self.stacked_widget.setCurrentIndex(0)
        self.show()
        QtCore.QTimer.singleShot(3000, self.show_main_window)

        self.ui_main.pushButton.clicked.connect(self.start_calibration)

    def show_main_window(self):
        self.stacked_widget.setCurrentIndex(1)
        self.ui_main.startAnimations() 
        
    def show_about_screen(self):
        self.stacked_widget.setCurrentWidget(self.about_screen)
        
    def show_settings_screen(self):
        # TODO
        # self.stacked_widget.setCurrentWidget(self.settings_screen)
        pass

    def start_calibration(self):
        self.hide()
        self.gaze_estimator.calibrate()
        BerhasilDialog.show_dialog(self)
        self.gaze_estimator.start()
        self.speech_recognition.start()
        
    def bring_to_top(self):
        self.show()
        self.raise_()
        self.activateWindow()
        
class TrayMenuDialog(QtWidgets.QDialog):
    def __init__(self, main_window: SplashScreenApp, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.ui = CardDialog()
        self.ui.setupUi(self)
        self.setup_behavior()
        
        # Make it frameless and transparent background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def setup_behavior(self):
        # Connect buttons to actions
        self.ui.pushButton.clicked.connect(self.main_window.show_about_screen)
        self.ui.pushButton_2.clicked.connect(self.toggle_microphone)
        self.ui.pushButton_3.clicked.connect(self.toggle_eye_tracking)
        self.ui.pushButton_4.clicked.connect(self.show_settings)

        # Make buttons checkable
        self.ui.pushButton_2.setCheckable(True)
        self.ui.pushButton_3.setCheckable(True)
        
        self.ui.pushButton_2.setChecked(self.main_window.speech_recognition._run_flag)
        self.ui.pushButton_3.setChecked(self.main_window.gaze_estimator._run_flag)

    def toggle_microphone(self):
        state = self.ui.pushButton_2.isChecked()
        self.ui.pushButton_2.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#A3D8FF' if state else 'white'};
                border-radius: 10px;
                border: 2px solid {'#4A8CB0' if state else '#9266CC'};
                font-family: 'Nunito', sans-serif;
                font-size: 14px;
                color: #333333;
            }}
        """)
        self.close()
        if state:
            self.main_window.speech_recognition.stop()
        else:
            self.main_window.speech_recognition.start()
            
    def showEvent(self, event):
        self.ui.pushButton_2.setChecked(self.main_window.speech_recognition.isRunning())
        super().showEvent(event)

    def toggle_eye_tracking(self):
        state = self.ui.pushButton_3.isChecked()
        self.ui.pushButton_3.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#A3D8FF' if state else 'white'};
                border-radius: 10px;
                border: 2px solid {'#4A8CB0' if state else '#9266CC'};
                font-family: 'Nunito', sans-serif;
                font-size: 14px;
                color: #333333;
            }}
        """)
        self.close()
        if state:
            self.main_window.gaze_estimator.stop()
        else:
            self.main_window.gaze_estimator.start()

    def show_settings(self):
        print("Showing settings...")
        self.close()

    def showEvent(self, event):
        # Position near system tray icon
        pos = QtGui.QCursor.pos()
        self.move(pos.x() - self.width()//2, pos.y() - self.height()//2)
        super().showEvent(event)

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
    def show_tray_menu():
        if not window.tray_menu or not window.tray_menu.isVisible():
            window.tray_menu = TrayMenuDialog(main_window=window)
            window.tray_menu.show()
    
    context_menu = QMenu()
    action_show = QAction("Show", context_menu)
    action_hide = QAction("Hide", context_menu)
    action_quit = QAction("Quit", context_menu)
    
    action_show.triggered.connect(window.bring_to_top)
    action_hide.triggered.connect(window.hide)
    action_quit.triggered.connect(app.quit)
    
    context_menu.addAction(action_show)
    context_menu.addAction(action_hide)
    context_menu.addSeparator()
    context_menu.addAction(action_quit)
    
    # Set context menu for right-click
    tray_icon.setContextMenu(context_menu)
    
    # Handle left-click for custom menu
    def handle_tray_click(reason):
        if reason == QSystemTrayIcon.Trigger:  # Left-click
            show_tray_menu()
    
    tray_icon.activated.connect(handle_tray_click)

    
    tray_icon.show()
    
    sys.exit(app.exec())
