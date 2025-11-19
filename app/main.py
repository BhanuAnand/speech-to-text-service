"""Main FastAPI application for speech-to-text service."""
import logging
import os
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.transcription import transcription_service

# Configure logging
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.service_name,
    description="Production-ready speech-to-text service using faster-whisper",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON response with service status
    """
    is_healthy = transcription_service.health_check()
    
    if is_healthy:
        return {
            "status": "ok",
            "service": settings.service_name,
            "model": settings.model_name,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy: model not loaded",
        )


@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe")
):
    """
    Transcribe an uploaded audio file.
    
    Args:
        file: Audio file (supported formats: WAV, MP3, M4A, OGG, FLAC, WebM)
        
    Returns:
        JSON response with transcript and metadata
        
    Raises:
        HTTPException: If file format is unsupported or transcription fails
    """
    # Validate content type
    if file.content_type not in settings.allowed_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file.content_type}. "
                   f"Supported formats: {', '.join(settings.allowed_formats)}",
        )
    
    # Save uploaded file temporarily
    temp_file_path: Optional[str] = None
    
    try:
        # Create unique filename
        file_extension = Path(file.filename or "audio").suffix or ".tmp"
        temp_file_path = os.path.join(
            settings.upload_dir,
            f"temp_{os.getpid()}_{id(file)}{file_extension}"
        )
        
        # Save file
        logger.info(f"Saving uploaded file: {file.filename}")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Check file size
        file_size = os.path.getsize(temp_file_path)
        if file_size > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large: {file_size} bytes. "
                       f"Maximum: {settings.max_file_size} bytes",
            )
        
        logger.info(f"File saved: {temp_file_path} ({file_size} bytes)")
        
        # Transcribe
        result = transcription_service.transcribe(temp_file_path)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result,
        )
        
    except HTTPException:
        raise
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}",
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up {temp_file_path}: {e}")


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": settings.service_name,
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe (POST)",
            "docs": "/docs",
        },
        "model": settings.model_name,
    }


def main():
    """Run the service."""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=False,
    )


if __name__ == "__main__":
    main()
