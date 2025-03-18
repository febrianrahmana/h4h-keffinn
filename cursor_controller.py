import pyautogui

class CursorController:
    def __init__(self, input_mode="command"):
        """
        Initialize the CursorController.
        :param input_mode: Mode of input, e.g., 'command' or 'text'.
        """
        self.input_mode = input_mode

    def handle_prompt(self, prompt):
        """Handles cursor actions based on the given prompt."""
        print(f"[{self.input_mode.upper()}] prompt: {prompt}")

        if prompt.startswith("mode"):
            if self.input_mode == "text":
                self.input_mode = "command"
            else:
                self.input_mode = "text"

        if self.input_mode == "text":
            pyautogui.write(prompt)
        else:
            prompt = prompt.lower().strip()

            if any(keyword in prompt for keyword in ("kiri kiri", "left left")):
                pyautogui.click()
                pyautogui.click()
            elif any(keyword in prompt for keyword in ("kiri", "left")):
                pyautogui.click()  # Left click
            elif any(keyword in prompt for keyword in ("kanan", "right")):
                pyautogui.rightClick()  # Right click
            else:
                print(f"Perintah '{prompt}' tidak dikenali.")


