import torch
import numpy as np
import speech_recognition as sr
from faster_whisper import WhisperModel

class SpeechRecognitionModel:
    def __init__(self, model_type="whisper"):
        self.model_type = model_type
        if model_type == "whisper":
            self.model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="int8")
        elif model_type == "google":
            self.recognizer = sr.Recognizer()
        else:
            raise ValueError("Unsupported model type. Choose 'whisper' or 'google'.")

    def transcribe(self, audio_chunk, language="id"):
        if self.model_type == "whisper":
            audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
            segments, _ = self.model.transcribe(audio_np, language=language, beam_size=10)
            filtered_segments = [
                segment
                for segment in segments
                if segment.no_speech_prob < 0.4
            ]
            for segment in filtered_segments:
                print(segment)

            return [segment.text.strip() for segment in filtered_segments]
        elif self.model_type == "google":
            audio_data = sr.AudioData(audio_chunk, 16000, 2)
            try:
                text = self.recognizer.recognize_google(audio_data, language=language)
                return [text] if text else []
            except sr.UnknownValueError:
                return []
            except sr.RequestError as e:
                print(f"Google Speech-to-Text API error: {e}")
                return []