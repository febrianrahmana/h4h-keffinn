import sys
import os
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, Signal, QParallelAnimationGroup
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QCheckBox, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import QFontDatabase, QCursor, QIcon, QFont

class SettingsButton(QWidget):
    clicked = Signal()
    
    def __init__(self, text, has_icon=False, icon_type=None, is_selected=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.has_icon = has_icon
        self.icon_type = icon_type  # "plus", "minus", "check"
        self.is_selected = is_selected
        self.is_hovered = False
        self.setupUI()
        
    def setupUI(self):
        self.setFixedHeight(40)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Text label
        self.text_label = QLabel(self.text)
        font = QFont("Nunito", 10)
        self.text_label.setFont(font)
        layout.addWidget(self.text_label)
        
        layout.addStretch()
        
        # Icon (plus, minus, or check)
        if self.has_icon:
            if self.icon_type == "plus":
                self.icon_label = QLabel("+")
            elif self.icon_type == "minus":
                self.icon_label = QLabel("−")
            elif self.icon_type == "check":
                self.icon_label = QLabel("✓")
            else:
                self.icon_label = QLabel("")
                
            self.icon_label.setStyleSheet("color: #333333; font-size: 14px;")
            layout.addWidget(self.icon_label)
        else:
            # Create an empty label for buttons that might later get an icon
            self.icon_label = QLabel("")
            self.icon_label.setStyleSheet("color: #333333; font-size: 14px;")
            layout.addWidget(self.icon_label)
        
        self.updateStyle()
    
    def updateStyle(self):
        if self.is_selected:
            bg_color = "#F0F0F0"
        elif self.is_hovered:
            bg_color = "#F5F5F5"
        else:
            bg_color = "#FFFFFF"
            
        text_color = "#333333"
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 5px;
            }}
            QLabel {{
                background-color: transparent;
                color: {text_color};
            }}
        """)
    
    def enterEvent(self, event):
        self.is_hovered = True
        self.updateStyle()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.is_hovered = False
        self.updateStyle()
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def setIconType(self, icon_type):
        self.icon_type = icon_type
        if icon_type == "plus":
            self.icon_label.setText("+")
        elif icon_type == "minus":
            self.icon_label.setText("−")
        elif icon_type == "check":
            self.icon_label.setText("✓")
        else:
            self.icon_label.setText("")


class CollapsibleSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = []
        self.setupUI()
        self.collapsed = True
        self.collapsible_height = 0
        
    def setupUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border-radius: 5px;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)
        
        # Container for collapsible content
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(1)
        self.content_widget.setMaximumHeight(0)
        
        self.main_layout.addWidget(self.content_widget)
    
    def addButton(self, text, has_icon=False, icon_type=None, is_selected=False):
        button = SettingsButton(text, has_icon, icon_type, is_selected)
        self.content_layout.addWidget(button)
        self.buttons.append(button)
        self.collapsible_height += button.height() + self.content_layout.spacing()
        return button
        
    def toggleCollapse(self, trigger_button=None):
        self.collapsed = not self.collapsed
        
        target_height = 0 if self.collapsed else self.collapsible_height
        
        # Update trigger button icon if provided
        if trigger_button:
            trigger_button.setIconType("plus" if self.collapsed else "minus")
        
        # Animate height change
        self.animation = QPropertyAnimation(self.content_widget, b"maximumHeight")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.content_widget.height())
        self.animation.setEndValue(target_height)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


class SettingsCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        # Set fixed size for the main card
        self.setFixedSize(280, 400)  # Increased height to accommodate expanded sections
        self.setStyleSheet("""
            QWidget#mainCard {
                background-color: white;
                border-radius: 10px;
            }
        """)
        self.setObjectName("mainCard")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add settings buttons
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(1)
        
        # Create main menu buttons
        self.btn_tentang = SettingsButton("Tentang EYE HEAR U")
        self.btn_microphone = SettingsButton("Microphone")
        self.btn_eye_tracking = SettingsButton("Eye Tracking")
        self.btn_settings = SettingsButton("Settings", True, "plus")
        
        # Settings sections (collapsible)
        self.settings_section = CollapsibleSection()
        
        # Speech Recognition section (collapsible)
        self.speech_section = CollapsibleSection()
        self.speech_header = SettingsButton("Speech Recognition", True, "plus")
        self.speech_normal = self.speech_section.addButton("Speech Recognition")
        self.speech_expanded = self.speech_section.addButton("Speech Recognition", True, "minus")
        self.subtitle_btn = self.speech_section.addButton("Subtitle")
        self.microphone_btn = self.speech_section.addButton("Microphone")
        self.model_btn = self.speech_section.addButton("Model", True, "plus")
        self.speech_eye_tracking = self.speech_section.addButton("Eye Tracking", True, "plus")
        
        # Eye Tracking section (collapsible)
        self.eye_section = CollapsibleSection()
        self.eye_header = SettingsButton("Eye Tracking", True, "plus")
        self.eye_normal = self.eye_section.addButton("Eye Tracking")
        self.eye_expanded = self.eye_section.addButton("Eye Tracking", True, "minus")
        self.pilihan_mata = self.eye_section.addButton("Pilihan Mata", True, "plus")
        self.kontrol_kepala = self.eye_section.addButton("Kontrol Kepala")
        
        # Add buttons to settings section
        self.speech_btn = self.settings_section.addButton("Speech Recognition", True, "plus")
        self.eye_tracking_menu = self.settings_section.addButton("Eye Tracking", True, "plus")
        
        # Connect signals
        self.btn_tentang.clicked.connect(self.toggleTentang)
        self.btn_microphone.clicked.connect(self.toggleMicrophone)
        self.btn_eye_tracking.clicked.connect(self.toggleEyeTracking)
        self.btn_settings.clicked.connect(self.toggleSettings)
        
        self.speech_btn.clicked.connect(self.showSpeechSection)
        self.eye_tracking_menu.clicked.connect(self.showEyeSection)
        
        self.speech_header.clicked.connect(self.toggleSpeechSection)
        self.eye_header.clicked.connect(self.toggleEyeSection)
        
        # Add buttons and sections to layout
        self.content_layout.addWidget(self.btn_tentang)
        self.content_layout.addWidget(self.btn_microphone)
        self.content_layout.addWidget(self.btn_eye_tracking)
        self.content_layout.addWidget(self.btn_settings)
        self.content_layout.addWidget(self.settings_section)
        
        # These are initially hidden and will be shown when needed
        self.speech_widget = QWidget()
        self.speech_layout = QVBoxLayout(self.speech_widget)
        self.speech_layout.setContentsMargins(0, 0, 0, 0)
        self.speech_layout.setSpacing(1)
        self.speech_layout.addWidget(self.speech_header)
        self.speech_layout.addWidget(self.speech_section)
        self.speech_widget.setVisible(False)
        
        self.eye_widget = QWidget()
        self.eye_layout = QVBoxLayout(self.eye_widget)
        self.eye_layout.setContentsMargins(0, 0, 0, 0)
        self.eye_layout.setSpacing(1)
        self.eye_layout.addWidget(self.eye_header)
        self.eye_layout.addWidget(self.eye_section)
        self.eye_widget.setVisible(False)
        
        self.content_layout.addWidget(self.speech_widget)
        self.content_layout.addWidget(self.eye_widget)
        
        main_layout.addWidget(self.content_widget)
        
    def toggleTentang(self):
        # Tentang doesn't get a checkmark
        pass
        
    def toggleMicrophone(self):
        # Toggle checkmark
        if self.btn_microphone.icon_type == "check":
            self.btn_microphone.setIconType("")
        else:
            self.btn_microphone.setIconType("check")
    
    def toggleEyeTracking(self):
        # Toggle checkmark
        if self.btn_eye_tracking.icon_type == "check":
            self.btn_eye_tracking.setIconType("")
        else:
            self.btn_eye_tracking.setIconType("check")
    
    def toggleSettings(self):
        # Toggle settings section visibility
        if self.settings_section.collapsed:
            # Hide speech and eye tracking sections
            self.speech_widget.setVisible(False)
            self.eye_widget.setVisible(False)
            
            # Show settings section
            self.settings_section.toggleCollapse(self.btn_settings)
        else:
            # Hide settings section
            self.settings_section.toggleCollapse(self.btn_settings)
    
    def showSpeechSection(self):
        # Hide settings section and show speech section
        self.settings_section.collapsed = True
        self.settings_section.content_widget.setMaximumHeight(0)
        self.btn_settings.setIconType("plus")
        
        # Show speech section widget
        self.speech_widget.setVisible(True)
        self.eye_widget.setVisible(False)
        self.speech_section.collapsed = True
        self.speech_section.toggleCollapse(self.speech_header)
    
    def showEyeSection(self):
        # Hide settings section and show eye tracking section
        self.settings_section.collapsed = True
        self.settings_section.content_widget.setMaximumHeight(0)
        self.btn_settings.setIconType("plus")
        
        # Show eye tracking section widget
        self.eye_widget.setVisible(True)
        self.speech_widget.setVisible(False)
        self.eye_section.collapsed = True
        self.eye_section.toggleCollapse(self.eye_header)
    
    def toggleSpeechSection(self):
        # Toggle speech section collapse
        self.speech_section.toggleCollapse(self.speech_header)
    
    def toggleEyeSection(self):
        # Toggle eye tracking section collapse
        self.eye_section.toggleCollapse(self.eye_header)


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("EYE HEAR U Settings")
        self.resize(300, 600)
        self.setStyleSheet("background-color: #F0F0F0;")
        
        # Load Nunito font if available
        font_path = os.path.join("src", "Nunito-Bold.otf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                app_font = QFont(font_family)
                QApplication.setFont(app_font)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add title label
        title_label = QLabel("Settings")
        title_label.setStyleSheet("color: #333333; font-size: 16px; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Create settings card
        self.settings_card = SettingsCard()
        main_layout.addWidget(self.settings_card, 0, Qt.AlignCenter | Qt.AlignTop)
        
        main_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsDialog()
    window.show()
    sys.exit(app.exec())