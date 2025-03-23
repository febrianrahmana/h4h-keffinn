from PySide6.QtCore import Signal, Slot, Qt, QThread
from voice_command.speech_processor import SpeechProcessor

class SpeechThread(QThread):
    def __init__(self):
        super().__init__()
        self._run_flag = False
        self.speech_processor = SpeechProcessor()
        
    def toggle(self):
        if not self._run_flag:
            self.run()
        else:
            self.stop()

    def run(self):
        self._run_flag = True
        self.speech_processor.listen()

    def stop(self):
        self._run_flag = False
        self.speech_processor.cleanup()
        self.wait()