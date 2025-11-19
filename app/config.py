"""Configuration management for the speech-to-text service."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Service settings
    service_name: str = "speech-to-text-service"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    
    # Model settings
    model_name: str = "base"  # tiny, base, small, medium, large
    model_device: str = "cpu"  # cpu or cuda
    compute_type: str = "int8"  # int8, float16, float32
    
    # Upload settings
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_formats: list[str] = [
        "audio/wav", "audio/wave", "audio/x-wav",
        "audio/mpeg", "audio/mp3",
        "audio/mp4", "audio/m4a",
        "audio/ogg",
        "audio/flac",
        "audio/webm",
    ]
    upload_dir: str = "uploads"
    
    class Config:
        env_prefix = "STT_"
        env_file = ".env"


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)
