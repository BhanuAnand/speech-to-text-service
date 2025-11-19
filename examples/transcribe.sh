#!/bin/bash
# Simple script to transcribe an audio file using the service

set -e

# Configuration
SERVICE_URL="${STT_SERVICE_URL:-http://localhost:8000}"
AUDIO_FILE="${1:-examples/sample.wav}"

# Check if file exists
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ Error: Audio file not found: $AUDIO_FILE"
    echo "Usage: $0 <audio-file>"
    exit 1
fi

echo "🎙️  Transcribing: $AUDIO_FILE"
echo "🌐 Service URL: $SERVICE_URL"
echo ""

# Detect content type from file extension
EXT="${AUDIO_FILE##*.}"
case "$EXT" in
    wav) CONTENT_TYPE="audio/wav" ;;
    mp3) CONTENT_TYPE="audio/mp3" ;;
    m4a) CONTENT_TYPE="audio/m4a" ;;
    ogg) CONTENT_TYPE="audio/ogg" ;;
    flac) CONTENT_TYPE="audio/flac" ;;
    webm) CONTENT_TYPE="audio/webm" ;;
    *) CONTENT_TYPE="audio/wav" ;;
esac

# Make request
response=$(curl -s -X POST "$SERVICE_URL/transcribe" \
    -F "file=@$AUDIO_FILE;type=$CONTENT_TYPE" \
    -H "Accept: application/json")

# Check if response is valid JSON
if echo "$response" | jq . > /dev/null 2>&1; then
    echo "📝 Transcript:"
    echo "$response" | jq -r '.transcript'
    echo ""
    echo "🌍 Language: $(echo "$response" | jq -r '.language')"
    echo "⏱️  Duration: $(echo "$response" | jq -r '.duration')s"
    echo ""
    echo "📊 Full response:"
    echo "$response" | jq .
else
    echo "❌ Error response:"
    echo "$response"
    exit 1
fi
