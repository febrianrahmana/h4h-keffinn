import pyaudio
import numpy as np
import torch
import traceback
from faster_whisper import WhisperModel
from cursor_controller import CursorController
import os
import sys
import threading
import time

class VoiceCursorController:
    def __init__(self, model_size="medium", input_mode="command"):
        self.model = WhisperModel(model_size, device="cuda" if torch.cuda.is_available() else "cpu", compute_type="int8")
        self.cursor_controller = CursorController(input_mode)
        self.chunk = 16000 
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)

    @staticmethod
    def is_silent(audio_np, silence_threshold=0.01):
        """Detect if the audio is silent by checking its RMS (Root Mean Square) energy."""
        rms = np.sqrt(np.mean(audio_np**2))
        return rms < silence_threshold

    @staticmethod
    def force_exit():
        """Force exit if the program hangs."""
        print("Forcing shutdown...")
        os._exit(1) 

    def listen(self):
        try:
            print("Listening... (Press Ctrl+C to stop)")
            while True:
                audio_chunk = self.stream.read(self.chunk, exception_on_overflow=False)
                audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0

                if self.is_silent(audio_np):
                    continue

                segments, _ = self.model.transcribe(audio_np, language="id", beam_size=10)

                for segment in segments:
                    text = segment.text.strip()

                    print(segment)

                    if segment.no_speech_prob > 0.7:
                        continue

                    if not text or len(text) < 3:
                        continue

                    self.cursor_controller.handle_prompt(text)

        except Exception as e:
            traceback.print_exc()
        except KeyboardInterrupt:
            print("Stopping...")

        finally:
            self.cleanup()

    def cleanup(self):
        """Stop streams and release resources."""
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        del self.model
        torch.cuda.empty_cache()
        print("Stopped.")

        time.sleep(1)
        active_threads = threading.enumerate()
        if len(active_threads) > 1:
            print(f"Active threads: {[t.name for t in active_threads]}")
            self.force_exit()
        sys.exit(0)

if __name__ == "__main__":
    voice_controller = VoiceCursorController(model_size="small", input_mode="command")
    voice_controller.listen()
