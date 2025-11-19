"""Speech-to-text transcription using OpenAI Whisper."""
import logging
import os
from pathlib import Path
from typing import Optional

import whisper

from app.config import settings

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for transcribing audio files using Whisper."""
    
    def __init__(self):
        """Initialize the transcription service with the Whisper model."""
        self.model: Optional[whisper.Whisper] = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Load the Whisper model."""
        try:
            logger.info(
                f"Loading Whisper model: {settings.model_name} "
                f"(device: {settings.model_device})"
            )
            self.model = whisper.load_model(
                settings.model_name,
                device=settings.model_device,
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcript and metadata
            
        Raises:
            RuntimeError: If transcription fails
        """
        if not self.model:
            raise RuntimeError("Model not initialized")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            logger.info(f"Transcribing audio file: {audio_path}")
            
            # Transcribe the audio
            result_obj = self.model.transcribe(audio_path)
            
            # Extract segments
            segment_list = []
            for segment in result_obj.get("segments", []):
                segment_list.append({
                    "start": round(segment["start"], 2),
                    "end": round(segment["end"], 2),
                    "text": segment["text"].strip(),
                })
            
            full_transcript = result_obj["text"].strip()
            detected_language = result_obj.get("language", "unknown")
            
            result = {
                "transcript": full_transcript,
                "language": detected_language,
                "language_probability": 1.0,  # openai-whisper doesn't provide this
                "duration": segment_list[-1]["end"] if segment_list else 0.0,
                "segments": segment_list,
            }
            
            logger.info(
                f"Transcription complete. Language: {detected_language}, "
                f"Duration: {result['duration']:.2f}s"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise RuntimeError(f"Transcription failed: {str(e)}")
    
    def health_check(self) -> bool:
        """Check if the service is healthy."""
        return self.model is not None


# Global transcription service instance
transcription_service = TranscriptionService()
