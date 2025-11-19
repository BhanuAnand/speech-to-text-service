"""Unit tests for transcription service."""
import os

import pytest

from app.transcription import TranscriptionService


def test_transcription_service_initialization():
    """Test that the transcription service initializes correctly."""
    service = TranscriptionService()
    assert service.model is not None
    assert service.health_check() is True


def test_transcribe_nonexistent_file():
    """Test transcription with a non-existent file."""
    service = TranscriptionService()
    
    with pytest.raises(FileNotFoundError):
        service.transcribe("nonexistent_file.wav")


def test_transcribe_valid_file(temp_audio_file):
    """Test transcription with a valid audio file."""
    service = TranscriptionService()
    
    result = service.transcribe(temp_audio_file)
    
    # Check result structure
    assert isinstance(result, dict)
    assert "transcript" in result
    assert "language" in result
    assert "duration" in result
    assert "segments" in result
    assert "language_probability" in result
    
    # Check types
    assert isinstance(result["transcript"], str)
    assert isinstance(result["language"], str)
    assert isinstance(result["duration"], (int, float))
    assert isinstance(result["segments"], list)


def test_health_check():
    """Test the health check functionality."""
    service = TranscriptionService()
    assert service.health_check() is True
    
    # Test with uninitialized model
    service.model = None
    assert service.health_check() is False
