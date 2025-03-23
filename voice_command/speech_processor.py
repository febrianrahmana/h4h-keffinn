import pyaudio
import numpy as np
import torch
import traceback
import os
import sys
import gc
import threading
import time
import atexit
import signal
import speech_recognition as sr
from faster_whisper import WhisperModel
from .cursor_controller import CursorController
from .speech_recognition_model import SpeechRecognitionModel

class SpeechProcessor:
    def __init__(self, model_type="whisper", input_mode="command"):
        self.model = None
        self.cursor_controller = None
        self.audio = None
        self.stream = None
        
        try:
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
            self.silence_threshold = 0.01
            
            print("Initializing PyAudio...")
            self.audio = pyaudio.PyAudio()
            
            # Register cleanup handlers
            atexit.register(self.cleanup)
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            print("Opening audio stream...")
            self.stream = self.audio.open(
                format=self.format, 
                channels=self.channels, 
                rate=self.rate, 
                input=True, 
                frames_per_buffer=self.chunk
            )
            print("Audio stream opened.")
        except Exception as e:
            print(f"Initialization error: {e}")
            traceback.print_exc()
            self.cleanup()
            raise

    @staticmethod
    def is_silent(audio_np, silence_threshold=0.01):
        rms = np.sqrt(np.mean(audio_np**2))
        return rms < silence_threshold

    def signal_handler(self, sig, frame):
        print(f"\nReceived signal {sig}")
        self.cleanup()
        sys.exit(0)

    def listen(self):
        try:
            print("Listening... (Press Ctrl+C to stop)")
            audio_buffer = b""  # Initialize an empty byte buffer
            
            while True:
                if not self.stream.is_active():
                    print("Audio stream is not active, reopening...")
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = self.audio.open(
                        format=self.format, 
                        channels=self.channels, 
                        rate=self.rate, 
                        input=True, 
                        frames_per_buffer=self.chunk
                    )
                
                audio_chunk = self.stream.read(self.chunk, exception_on_overflow=False)
                audio_buffer += audio_chunk
                audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0

                if self.is_silent(audio_np, self.silence_threshold):
                    if len(audio_buffer) > 0:
                        print("Processing accumulated audio...")
                        texts = self.model.transcribe(audio_buffer, language="id")
                        for text in texts:
                            print(text)
                            self.cursor_controller.handle_prompt(text)
                        audio_buffer = b""  # Reset buffer
                        
                # Add a small delay to reduce CPU usage
                time.sleep(0.01)

        except Exception as e:
            print(f"Error in listen: {e}")
            traceback.print_exc()
        finally:
            self.cleanup()

    def cleanup(self):
        print("Performing cleanup...")
        
        # Close audio stream
        if hasattr(self, 'stream') and self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
                self.stream = None
                print("Audio stream closed.")
            except Exception as e:
                print(f"Error closing stream: {e}")
        
        # Terminate PyAudio
        if hasattr(self, 'audio') and self.audio:
            try:
                self.audio.terminate()
                self.audio = None
                print("PyAudio terminated.")
            except Exception as e:
                print(f"Error terminating PyAudio: {e}")
        
        # Clean up model resources
        if hasattr(self, 'model') and self.model:
            try:
                del self.model
                self.model = None
                print("Model deleted.")
            except Exception as e:
                print(f"Error deleting model: {e}")
        
        # Clean up CUDA memory
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print("CUDA cache emptied.")
        except Exception as e:
            print(f"Error emptying CUDA cache: {e}")
        
        # Force garbage collection
        try:
            gc.collect()
            print("Garbage collection performed.")
        except Exception as e:
            print(f"Error in garbage collection: {e}")
        
        print("Cleanup completed.")

if __name__ == "__main__":
    try:
        voice_controller = SpeechProcessor(model_type="google", input_mode="command")
        voice_controller.listen()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        # Allow time for resources to be released
        time.sleep(1)
        sys.exit(1)