# Speech-to-Text Service

A speech-to-text service using FastAPI and OpenAI Whisper.

## Architecture Overview

This service provides a REST API for transcribing audio files using OpenAI's Whisper model. FastAPI handles HTTP requests, Whisper processes the audio with configurable model sizes (tiny to large), and the service returns structured JSON with transcripts and metadata (language, duration, segments). Docker provides containerization, pytest handles testing, and GitHub Actions manages CI/CD.

## How to Run Locally

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

GET /health - Returns {"status": "ok", "service": "speech-to-text-service", "model": "base"}

POST /transcribe - Upload audio file, returns JSON transcript

Response format:
```json
{
  "transcript": "Full transcript text here",
  "language": "en",
  "duration": 5.23,
  "segments": [{"start": 0.0, "end": 2.5, "text": "..."}]
}
```

Supported formats: WAV, MP3, M4A, OGG, FLAC, WebM
File size limit: 100MB (configurable via STT_MAX_FILE_SIZE)

Errors:
- 400 - Unsupported format or missing file
- 413 - File too large
- 500 - Transcription failed

## Example Usage

```bash
# Check health
curl http://localhost:8000/health

# Transcribe audio file
curl -X POST http://localhost:8000/transcribe -F "file=@audio.wav"

# Using the provided script with real speech
./examples/transcribe.sh examples/harvard.wav

# Or with the tone sample
./examples/transcribe.sh examples/sample.wav
```

**Note:** Use `harvard.wav` for real speech transcription. The `sample.wav` is just a test tone.

## Testing

```bash
# Activate venv if not already activated
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest --cov=app
```

## Try It Live

The service is publicly accessible at: **`https://lissom-supersensitive-darien.ngrok-free.dev`**

Test the live demo:
```bash
# Health check
curl https://lissom-supersensitive-darien.ngrok-free.dev/health

# Transcribe audio (using harvard.wav for real speech)
curl -X POST https://lissom-supersensitive-darien.ngrok-free.dev/transcribe \
  -F "file=@examples/harvard.wav;type=audio/wav"

# Or use the test script
./test-public-service.sh
```

## CI/CD

GitHub Actions runs tests and builds Docker image on push. See `.github/workflows/ci.yml`.

## Trade-offs & Next Steps

Trade-offs:
- Used openai-whisper for simplicity and wide compatibility
- File uploads instead of streaming (simpler, good enough for most cases)
- Synchronous processing (minimal implementation; would add job queue for scale)
- Models download on first use (faster Docker builds, slower first request)

What I'd add next:
- WebSocket API for streaming/real-time transcription
- Job queue (Redis + Celery) for async processing
- Rate limiting and authentication
- Pre-load models in Docker image
