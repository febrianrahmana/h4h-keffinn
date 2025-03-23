import pyautogui
import subprocess
import platform
import os
import signal
import time
import psutil
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class SubtitleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtitles")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set initial size and position
        screen_rect = QApplication.primaryScreen().geometry()
        window_width = int(screen_rect.width() * 0.8)  # 80% of screen width
        window_height = 80
        
        x = (screen_rect.width() - window_width) // 2
        y = screen_rect.height() - window_height - 50  # 50 pixels from bottom
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Create subtitle label
        self.subtitle_label = QLabel(self)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 180);"
            "color: white;"
            "border-radius: 10px;"
            "padding: 5px;"
        )
        self.subtitle_label.setFont(QFont("Arial", 14))
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setGeometry(0, 0, window_width, window_height)
        
        # Setup timer for auto-clearing
        self.clear_timer = QTimer(self)
        self.clear_timer.timeout.connect(self.clear_subtitle)
        
        # Variables for dragging
        self.dragging = False
        self.offset = None
    
    def show_text(self, text, duration=3000):
        """Display text and start timer to clear it"""
        self.subtitle_label.setText(text)
        
        # Reset timer
        self.clear_timer.stop()
        self.clear_timer.start(duration)
    
    def clear_subtitle(self):
        """Clear the subtitle text"""
        self.subtitle_label.setText("")
        self.clear_timer.stop()
    
    # Override mouse events for dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToGlobal(event.position().toPoint()) - self.offset)


class CursorController:
    def __init__(self, input_mode="command"):
        """
        Initialize the CursorController.
        :param input_mode: Mode of input, e.g., 'command' or 'text'.
        """
        self.input_mode = input_mode
        self.hold_mode = False
        self.keyboard_process = None
        
        # Initialize PySide6 App and subtitle window
        self.app = QApplication.instance() or QApplication([])
        self.subtitle_window = SubtitleWindow()
        self.subtitle_duration = 3000  # Duration in milliseconds to show each subtitle
        
        # Automatically show the subtitle window
        self.subtitle_window.show()
        self.subtitle_window.show_text("Voice Control Ready", 2000)
        
    def handle_prompt(self, prompt):
        """Handles cursor actions based on the given prompt."""
        print(f"[{self.input_mode.upper()}] prompt: {prompt}")

        # Always display the prompt as a subtitle
        self.show_subtitle(prompt)

        prompt_parsed = prompt.lower().strip()

        if prompt_parsed.startswith("write") or prompt_parsed.startswith("tulis"):
            text_to_write = prompt[5:].strip()
            if text_to_write:
                print(text_to_write)
                pyautogui.write(text_to_write)
                return
            
        if any(keyword in prompt_parsed for keyword in ("command", "perintah")):
            self.input_mode = "command"
            return
        
        if any(keyword in prompt_parsed for keyword in ("text", "teks")):
            self.input_mode = "text"
            return
        
        if prompt_parsed.startswith("mode"):
            if self.input_mode == "text":
                self.input_mode = "command"
            else:
                self.input_mode = "text"
            return
        
        if "hold" in prompt_parsed:
            self.hold_mode = not self.hold_mode
            if self.hold_mode:
                print("Hold mode activated")
                pyautogui.mouseDown()
            else:
                print("Hold mode deactivated")
                pyautogui.mouseUp()
            return
        
        if any(keyword in prompt_parsed for keyword in ("space", "spasi")):
            pyautogui.press("space")
            return
        if any(keyword in prompt_parsed for keyword in ("capslock", "kapital")):
            pyautogui.press("capslock")
            return
        if any(keyword in prompt_parsed for keyword in ("back", "kembali")):
            pyautogui.press("backspace")
            return
        if any(keyword in prompt_parsed for keyword in ("control", "kontrol")):
            pyautogui.press("ctrl")
            return
        if any(keyword in prompt_parsed for keyword in ("enter", "masuk")):
            pyautogui.press("enter")
            return
        if any(keyword in prompt_parsed for keyword in ("shift", "geser")):
            pyautogui.press("shift")
        
        if self.input_mode == "text":
            pyautogui.write(prompt)
            return
        
        prompt = prompt.lower().strip()

        if any(keyword in prompt for keyword in ("klik klik", "click click")):
            pyautogui.click()
            pyautogui.click()
        elif any(keyword in prompt for keyword in ("klik", "click")):
            pyautogui.click()
        elif any(keyword in prompt for keyword in ("kanan", "right")):
            pyautogui.rightClick()
        elif "keyboard" in prompt:
            if self.is_keyboard_running():
                self.close_onscreen_keyboard()
            else:
                self.show_onscreen_keyboard()
        else:
            print(f"Perintah '{prompt}' tidak dikenali.")
    
    def show_subtitle(self, text):
        """Display the given text as a subtitle"""
        self.subtitle_window.show_text(text, self.subtitle_duration)
        
        self.app.processEvents()

    def is_keyboard_running(self):
        """Check if the on-screen keyboard is currently running."""
        os_name = platform.system()
        if os_name == "Windows":
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'osk.exe':
                    return True
        elif os_name == "Darwin":
            for proc in psutil.process_iter(['pid', 'name']):
                if "Keyboard Viewer" in proc.info['name']:
                    return True
        elif os_name == "Linux":
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'onboard':
                    return True
                
        return False

    def show_onscreen_keyboard(self):
        """Displays the on-screen keyboard based on the operating system."""
        os_name = platform.system()
        try:
            if os_name == "Windows":
                subprocess.Popen("osk.exe", shell=True)
            elif os_name == "Darwin":  # macOS
                subprocess.Popen(["open", "/System/Applications/Utilities/Keyboard Viewer.app"])
            elif os_name == "Linux":
                subprocess.Popen(["onboard"])
            else:
                print(f"On-screen keyboard not supported on {os_name}.")
                
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 4, screen_height // 4)
            
        except FileNotFoundError:
            print("On-screen keyboard application not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close_onscreen_keyboard(self):
        """Closes the on-screen keyboard."""
        os_name = platform.system()
        try:
            if os_name == "Windows":
                os.system("taskkill /f /im osk.exe")
            elif os_name == "Darwin":
                os.system("pkill -f 'Keyboard Viewer'")
            elif os_name == "Linux":
                os.system("pkill onboard")
            print("Keyboard Closed")
        except Exception as e:
            print(f"Error closing keyboard: {e}")