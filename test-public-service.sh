#!/bin/bash
# Test the publicly deployed service

if [ -z "$1" ]; then
    echo "Usage: $0 <NGROK_URL>"
    echo "Example: $0 https://abc123.ngrok-free.app"
    exit 1
fi

SERVICE_URL="$1"

echo "🌐 Testing service at: $SERVICE_URL"
echo ""

# Test health
echo "1️⃣  Testing /health endpoint..."
curl -s "$SERVICE_URL/health" | jq .
echo ""

# Test transcription
echo "2️⃣  Testing /transcribe endpoint with harvard.wav..."
curl -s -X POST "$SERVICE_URL/transcribe" \
    -F "file=@examples/harvard.wav;type=audio/wav" | jq .
echo ""

echo "✅ Tests complete!"
