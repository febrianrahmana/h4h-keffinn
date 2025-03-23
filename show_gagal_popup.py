import sys
import os
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QFontDatabase
from gagal_popup import Ui_Dialog  # from generated .py
import icons_rc  # already compiled earlier

class GagalPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Load Nunito font
        font_id = QFontDatabase.addApplicationFont(os.path.join("src", "Nunito-Bold.otf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Nunito"

        # Set label font
        label_font = self.ui.label.font()
        label_font.setFamily(font_family)
        label_font.setPointSize(48)
        label_font.setBold(True)
        self.ui.label.setFont(label_font)

        # Set button style
        self.ui.pushButton.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb(255, 255, 255);
                border-radius: 20px;
                color: #4A8CB0;
                font-size: 25px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GagalPopup()
    window.exec_()
