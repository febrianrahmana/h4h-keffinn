from PySide6.QtCore import Signal, Slot, Qt, QThread
from voice_command.speech_processor import SpeechProcessor

class SpeechThread(QThread):
    def __init__(self, speech_processor: SpeechProcessor):
        super().__init__()
        self.speech_processor = speech_processor

    def run(self):
        self.speech_processor.listen()

    def stop(self):
        self.speech_processor.cleanup()
        self.wait()