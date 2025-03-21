import pyaudio
import numpy as np
import torch
import traceback
import os
import sys
import threading
import time
import speech_recognition as sr
from faster_whisper import WhisperModel
from cursor_controller import CursorController
from speech_recognition_model import SpeechRecognitionModel

class VoiceController:
    def __init__(self, model_type="whisper", input_mode="command"):
        print("Initializing SpeechRecognitionModel...")
        self.model = SpeechRecognitionModel(model_type)
        print("SpeechRecognitionModel initialized.")

        print("Initializing CursorController...")
        self.cursor_controller = CursorController(input_mode)
        print("CursorController initialized.")

        print("Setting audio parameters...")
        self.chunk = 16000 
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

        print("Initializing PyAudio...")
        self.audio = pyaudio.PyAudio()
        print("Opening audio stream...")
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        print("Audio stream opened.")

    @staticmethod
    def is_silent(audio_np, silence_threshold=0.01):
        rms = np.sqrt(np.mean(audio_np**2))
        return rms < silence_threshold

    @staticmethod
    def force_exit():
        print("Forcing shutdown...")
        os._exit(1)

    def listen(self):
        try:
            print("Listening... (Press Ctrl+C to stop)")
            while True:
                audio_chunk = self.stream.read(self.chunk, exception_on_overflow=False)
                texts = self.model.transcribe(audio_chunk, language="en")

                for text in texts:
                    print(text)
                    self.cursor_controller.handle_prompt(text)
        except Exception as e:
            traceback.print_exc()
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.cleanup()

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        # del self.model
        torch.cuda.empty_cache()
        print("Stopped.")
        # time.sleep(1)
        active_threads = threading.enumerate()
        if len(active_threads) > 1:
            print(f"Active threads: {[t.name for t in active_threads]}")
            self.force_exit()
        sys.exit(0)

if __name__ == "__main__":
    voice_controller = VoiceController(model_type="whisper", input_mode="command")
    voice_controller.listen()
