import torch
import numpy as np
import speech_recognition as sr
from faster_whisper import WhisperModel
import gc

class SpeechRecognitionModel:
    def __init__(self, model_type="google"):
        self.model_type = model_type
        self.model = None
        self.recognizer = None
        
        # Force cleanup before initializing
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        try:
            if model_type == "whisper":
                # Set compute_type based on available hardware
                if torch.cuda.is_available():
                    print("Using CUDA for WhisperModel")
                    self.model = WhisperModel(
                        "medium", 
                        device="cuda", 
                        compute_type="int8",
                    )
                else:
                    print("Using CPU for WhisperModel")
                    self.model = WhisperModel(
                        "medium", 
                        device="cpu", 
                        compute_type="int8",
                    )
            elif model_type == "google":
                self.recognizer = sr.Recognizer()
            else:
                raise ValueError("Unsupported model type. Choose 'whisper' or 'google'.")
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.cleanup()
            raise

    def transcribe(self, audio_chunk, language="id"):
        try:
            if self.model_type == "whisper":
                # Ensure audio chunk is properly formatted - normalize once
                if isinstance(audio_chunk, bytes):
                    audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
                else:
                    # Already a numpy array
                    audio_np = audio_chunk
                
                # Add timing for debugging
                start_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
                end_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
                
                if start_time:
                    start_time.record()
                
                # Run transcription with optimized parameters
                segments, _ = self.model.transcribe(
                    audio_np, 
                    language=language, 
                    beam_size=5,  # Reduced from 10 for speed
                    vad_filter=True,  # Enable Voice Activity Detection
                    vad_parameters={"threshold": 0.5}
                )
                
                # Convert generator to list to avoid issues
                segments_list = list(segments)
                
                if end_time:
                    end_time.record()
                    torch.cuda.synchronize()
                    print(f"Transcription took {start_time.elapsed_time(end_time):.2f} ms")
                
                # Filter out segments with high no_speech probability
                filtered_segments = [
                    segment
                    for segment in segments_list
                    if segment.no_speech_prob < 0.4
                ]
                
                # Free up GPU memory
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
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
        except Exception as e:
            print(f"Transcription error: {e}")
            return []

    def cleanup(self):
        """Release all resources"""
        try:
            # Clean up model
            if self.model_type == "whisper" and self.model:
                del self.model
                self.model = None
            
            # Force garbage collection
            gc.collect()
            
            # Clear CUDA cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            print("SpeechRecognitionModel resources released")
        except Exception as e:
            print(f"Error during model cleanup: {e}")
            
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()