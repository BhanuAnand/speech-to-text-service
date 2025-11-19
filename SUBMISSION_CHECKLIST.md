# Submission Checklist

Before submitting to ZoomInfo, complete these steps:

## 1. Deploy Service Publicly with ngrok

```bash
# Terminal 1: Start the service
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Expose publicly
ngrok http 8000
```

**Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`)

## 2. Update README.md

Replace `<YOUR_NGROK_URL>` in the README with your actual ngrok URL:
- Line ~106: Update the "Service is live at" section

## 3. Test End-to-End

```bash
# Replace with YOUR actual ngrok URL
export NGROK_URL="https://YOUR-ACTUAL-URL.ngrok-free.app"

# Test health
curl $NGROK_URL/health

# Test transcription
curl -X POST $NGROK_URL/transcribe -F "file=@examples/harvard.wav;type=audio/wav"
```

## 4. Commit and Push to GitHub

```bash
git add .
git commit -m "Add public deployment with ngrok"
git push origin main
```

## 5. Prepare Submission

**Send to ZoomInfo:**
1. GitHub repository URL
2. Public service URL (ngrok URL)
3. Instructions: "Service is deployed and accessible at <ngrok-url>. See README for usage examples."

## 6. Keep Service Running

⚠️ **IMPORTANT:** Keep both terminals running (service + ngrok) until ZoomInfo reviews your submission!

## What They'll Check

✅ Clone your repo  
✅ Read the README  
✅ Access your public URL/health endpoint  
✅ POST an audio file to /transcribe  
✅ Verify they get a transcript back  
✅ Check CI/CD runs on GitHub  
✅ Review code quality and tests  

## Notes

- ngrok free tier URL expires when you close it
- Keep the service running during their review window
- If they can't reach it, they may ask you to restart
