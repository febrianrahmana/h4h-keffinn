import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QFontDatabase
from berhasil_popup import Ui_Dialog  # This is the compiled .ui file

class SuccessPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Load custom font
        font_id = QFontDatabase.addApplicationFont(os.path.join("src", "Nunito-Bold.otf"))
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Nunito"

        # Apply to label
        label_font = self.ui.label.font()
        label_font.setFamily(font_family)
        label_font.setPointSize(48)
        self.ui.label.setFont(label_font)

        # Apply to button
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
    window = SuccessPopup()
    window.show()
    sys.exit(app.exec_())
