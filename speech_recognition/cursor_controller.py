import pyautogui
import subprocess
import platform
import os
import signal
import time
import psutil

class CursorController:
    def __init__(self, input_mode="command"):
        """
        Initialize the CursorController.
        :param input_mode: Mode of input, e.g., 'command' or 'text'.
        """
        self.input_mode = input_mode
        self.hold_mode = False  # Add hold mode attribute
        self.keyboard_process = None  # Store the keyboard process
        
    def handle_prompt(self, prompt):
        """Handles cursor actions based on the given prompt."""
        print(f"[{self.input_mode.upper()}] prompt: {prompt}")

        prompt_parsed = prompt.lower().strip()

        if prompt_parsed.startswith("escape"):
            text_to_write = prompt[len("escape"):].strip()
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
        
        if "hold" in prompt_parsed: #toggle hold mode
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
        if any(keyword in prompt_parsed for keyword in ("cap", "kap")):
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
            return
        
        if self.input_mode == "text":
            pyautogui.write(prompt)
            return
        
        prompt = prompt.lower().strip()

        if any(keyword in prompt for keyword in ("kiri kiri", "left left")):
            pyautogui.click()
            pyautogui.click()
        elif any(keyword in prompt for keyword in ("kiri", "left")):
            pyautogui.click()  # Left click
        elif any(keyword in prompt for keyword in ("kanan", "right")):
            pyautogui.rightClick()  # Right click
        elif "keyboard" in prompt:
            if self.is_keyboard_running():
                self.close_onscreen_keyboard()
            else:
                self.show_onscreen_keyboard()
        else:
            print(f"Perintah '{prompt}' tidak dikenali.")

    def is_keyboard_running(self):
        """Check if the on-screen keyboard is currently running."""
        os_name = platform.system()
        if os_name == "Windows":
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'osk.exe':
                    return True
        elif os_name == "Darwin":  # macOS
            # Check for Keyboard Viewer process
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
                subprocess.Popen("osk.exe", shell=True)  # Windows on-screen keyboard
            elif os_name == "Darwin":  # macOS
                subprocess.Popen(["open", "/System/Applications/Utilities/Keyboard Viewer.app"])
            elif os_name == "Linux":
                subprocess.Popen(["onboard"]) # most common linux on screen keyboard
            else:
                print(f"On-screen keyboard not supported on {os_name}.")
                
            # Click away from keyboard to allow other clicks to work
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
            elif os_name == "Darwin":  # macOS
                os.system("pkill -f 'Keyboard Viewer'")
            elif os_name == "Linux":
                os.system("pkill onboard")
            print("Keyboard Closed")
        except Exception as e:
            print(f"Error closing keyboard: {e}")