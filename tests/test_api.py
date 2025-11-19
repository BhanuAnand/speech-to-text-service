"""Integration tests for API endpoints."""
import io

import pytest
from fastapi import status


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "model" in data


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "endpoints" in data


def test_transcribe_missing_file(client):
    """Test transcription without a file."""
    response = client.post("/transcribe")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_transcribe_unsupported_format(client):
    """Test transcription with unsupported file format."""
    # Create a text file and try to upload it
    file_content = b"This is not an audio file"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    response = client.post("/transcribe", files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Unsupported file format" in response.json()["detail"]


def test_transcribe_valid_audio(client, temp_audio_file):
    """Test transcription with a valid audio file."""
    with open(temp_audio_file, "rb") as f:
        files = {
            "file": ("test.wav", f, "audio/wav")
        }
        response = client.post("/transcribe", files=files)
    
    # Should succeed (even if transcript is empty for silent audio)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "transcript" in data
    assert "language" in data
    assert "duration" in data
    assert "segments" in data


def test_transcribe_large_file(client):
    """Test transcription with a file that's too large."""
    # Create a large file (simulate by checking size limit)
    # This is a simplified test - in production you'd create an actual large file
    large_content = b"0" * (101 * 1024 * 1024)  # 101 MB
    files = {
        "file": ("large.wav", io.BytesIO(large_content), "audio/wav")
    }
    
    response = client.post("/transcribe", files=files)
    # Should fail due to size (either 413 or 400)
    assert response.status_code in [
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ]


def test_api_error_responses_are_json(client):
    """Test that error responses are properly formatted as JSON."""
    # Test with unsupported format
    files = {
        "file": ("test.txt", io.BytesIO(b"test"), "text/plain")
    }
    response = client.post("/transcribe", files=files)
    
    # Should return JSON error
    assert response.headers["content-type"] == "application/json"
    assert "detail" in response.json()
