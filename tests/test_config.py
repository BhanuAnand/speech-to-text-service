"""Unit tests for configuration."""
import os

from app.config import Settings


def test_default_settings():
    """Test default settings values."""
    settings = Settings()
    
    assert settings.service_name == "speech-to-text-service"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.log_level == "info"
    assert settings.model_name == "base"
    assert settings.model_device == "cpu"
    assert settings.compute_type == "int8"
    assert settings.max_file_size == 100 * 1024 * 1024


def test_allowed_formats():
    """Test that allowed formats are configured."""
    settings = Settings()
    
    assert len(settings.allowed_formats) > 0
    assert "audio/wav" in settings.allowed_formats
    assert "audio/mp3" in settings.allowed_formats
    assert "audio/mpeg" in settings.allowed_formats


def test_env_prefix():
    """Test that environment variables use correct prefix."""
    # Set an environment variable
    os.environ["STT_MODEL_NAME"] = "small"
    
    settings = Settings()
    assert settings.model_name == "small"
    
    # Cleanup
    del os.environ["STT_MODEL_NAME"]
