# 🎥 Awaaz Demo Guide - Complete Testing & Video Recording

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Environment

```bash
# Go to your project
cd ~/aiforbharat\ hackathon/AWAAZ/backend

# Create .env file (if not done)
cp .env.example .env
nano .env
```

**Add these credentials:**
```env
AWS_ACCESS_KEY_ID=your_new_key
AWS_SECRET_ACCESS_KEY=your_new_secret
AWS_REGION=us-east-1

AWAAZ_DOCUMENTS_BUCKET=awaaz-docs-demo
AWAAZ_SCHEMES_BUCKET=awaaz-schemes-demo
AWAAZ_GENERATED_BUCKET=awaaz-generated-demo

BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_REGION=us-east-1
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start Backend

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 4: Open Frontend

```bash
# In a new terminal
cd ~/aiforbharat\ hackathon/AWAAZ/frontend

# Open in browser (use one of these)
open index.html                    # Mac
python3 -m http.server 5500        # Or start simple server
```

---

## ✅ Testing Checklist (Before Recording)

### Test 1: Backend Health Check

Open browser: http://localhost:8000/health

**Expected Response:**
```json
{
  "status": "healthy",
  "aws_configured": true,
  "bhashini_configured": false
}
```

### Test 2: API Documentation

Open: http://localhost:8000/docs

You should see interactive API documentation with all endpoints.

### Test 3: Chat API

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am a farmer with 2 acres of land",
    "language": "en"
  }'
```

**Expected Response:**
```json
{
  "reply": "Good news! You may be eligible for PM Kisan scheme...",
  "schemes": ["PM Kisan"],
  "next_step": "document_upload"
}
```

### Test 4: Document Upload (OCR)

**Using curl:**
```bash
# Upload a test image (Aadhaar card)
curl -X POST http://localhost:8000/api/upload-document \
  -F "file=@/path/to/aadhaar.jpg" \
  -F "document_type=aadhaar"
```

**Expected Response:**
```json
{
  "document_type": "aadhaar",
  "verified": true,
  "name": "Ram Kumar",
  "document_number": "123456789012",
  "clarity_score": 0.95
}
```

### Test 5: Generate Affidavit

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/generate-affidavit \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Ram Kumar",
    "father_name": "Shyam Kumar",
    "address": "Village Rampur, District Sitapur",
    "purpose": "Income Certificate",
    "language": "en"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "pdf_path": "./output/affidavit_20240308_123456.pdf",
  "message": "Affidavit generated successfully"
}
```

---

## 🎬 Demo Video Script (5-7 Minutes)

### Scene 1: Introduction (30 seconds)

**What to show:**
- Project title slide
- Problem statement: "Helping Indian citizens access government schemes"

**What to say:**
> "Awaaz is an AI-powered assistant that helps Indian citizens discover and apply for government schemes through voice and text interaction."

---

### Scene 2: Architecture Overview (45 seconds)

**What to show:**
- Show the architecture diagram: `awaaz-architecture.png`
- Highlight key components

**What to say:**
> "Our system uses Amazon Bedrock for AI reasoning, Textract for document OCR, and S3 for storage. The frontend is a simple WhatsApp-style interface, and the backend is built with FastAPI."

---

### Scene 3: Live Demo - Chat Interface (1.5 minutes)

**What to show:**
1. Open frontend (http://localhost:5500)
2. Type: "I am a farmer with 2 acres of land"
3. Show AI response suggesting PM Kisan scheme
4. Type: "Tell me more about PM Kisan"
5. Show detailed explanation

**What to say:**
> "Users can simply describe their situation in natural language. Our AI, powered by Amazon Bedrock, understands the context and matches them with relevant schemes."

---

### Scene 4: Document Verification (1.5 minutes)

**What to show:**
1. Click "Upload Document" button
2. Upload sample Aadhaar card image
3. Show OCR processing (loading indicator)
4. Display extracted information:
   - Name
   - Aadhaar number
   - Address
   - Verification status

**What to say:**
> "Users can upload their documents directly. We use Amazon Textract for OCR, which is specifically trained on Indian government documents like Aadhaar, PAN, and voter ID cards."

---

### Scene 5: Form Generation (1 minute)

**What to show:**
1. Click "Generate Application Form"
2. Show pre-filled form with user data
3. Click "Generate Affidavit"
4. Show generated PDF
5. Display download option

**What to say:**
> "Once documents are verified, users can generate pre-filled application forms and affidavits automatically. These are stored securely in AWS S3."

---

### Scene 6: Voice Interaction (Optional - 1 minute)

**What to show:**
1. Click microphone button
2. Speak: "Mujhe kisan yojana chahiye"
3. Show transcription
4. Show AI response in Hindi
5. Play text-to-speech response

**What to say:**
> "For users with low digital literacy, we support voice interaction in multiple Indian languages using the Bhashini API."

---

### Scene 7: Backend & Code (1 minute)

**What to show:**
1. Show VS Code with project structure
2. Highlight key files:
   - `services/ocr_service.py`
   - `services/pdf_generator.py`
   - `services/scheme_engine.py`
3. Show API documentation (http://localhost:8000/docs)

**What to say:**
> "The backend is modular and scalable. We have separate services for OCR, PDF generation, and AI scheme matching. All APIs are well-documented using FastAPI's automatic documentation."

---

### Scene 8: AWS Integration (45 seconds)

**What to show:**
1. Open AWS Console
2. Show S3 buckets with uploaded documents
3. Show Bedrock model access
4. Show CloudWatch logs (optional)

**What to say:**
> "We leverage AWS services for scalability and reliability. Documents are stored in S3, AI reasoning uses Bedrock, and OCR is powered by Textract."

---

### Scene 9: Conclusion (30 seconds)

**What to show:**
- Summary slide with key features
- GitHub repo link
- Team credits

**What to say:**
> "Awaaz makes government schemes accessible to everyone, regardless of their digital literacy. It's voice-first, multilingual, and powered by cutting-edge AI. Thank you!"

---

## 🎥 Recording Tips

### Tools to Use:
- **Screen Recording**: QuickTime (Mac), OBS Studio, or Loom
- **Video Editing**: iMovie, DaVinci Resolve, or Kapwing
- **Audio**: Use a good microphone or AirPods

### Best Practices:
1. **Close unnecessary apps** - Clean desktop
2. **Use full screen** - Hide menu bars
3. **Slow down** - Give viewers time to see what's happening
4. **Zoom in** - Make text readable
5. **Practice first** - Do a dry run
6. **Add captions** - For accessibility
7. **Background music** - Subtle, not distracting

### Screen Layout:
```
┌─────────────────────────────────┐
│  Browser (Frontend)             │
│  http://localhost:5500          │
│                                 │
│  [Show user interactions here]  │
│                                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  Terminal (Backend Logs)        │
│  Show API calls in real-time    │
└─────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process
kill -9 <PID>

# Restart
uvicorn main:app --reload
```

### AWS errors
```bash
# Test AWS connection
python -c "import boto3; print(boto3.client('s3').list_buckets())"

# Check .env file
cat .env
```

### Frontend not connecting
```bash
# Check CORS settings in main.py
# Make sure allow_origins includes your frontend URL
```

### OCR not working
```bash
# Test Textract
python -c "from config.aws_config import aws_config; print(aws_config.textract_client)"
```

---

## 📊 Demo Data

### Sample User Profiles:

**Farmer:**
```json
{
  "name": "Ram Kumar",
  "occupation": "farmer",
  "income": "1.5 lakh",
  "land": "2 acres",
  "state": "Uttar Pradesh"
}
```

**Student:**
```json
{
  "name": "Priya Sharma",
  "occupation": "student",
  "age": 20,
  "category": "SC",
  "state": "Maharashtra"
}
```

**Senior Citizen:**
```json
{
  "name": "Ramesh Patel",
  "age": 65,
  "income": "No income",
  "state": "Gujarat"
}
```

### Sample Documents:
- Create fake Aadhaar card using Canva
- Use sample PAN card template
- Generate test income certificate

---

## ✅ Pre-Recording Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5500
- [ ] AWS credentials configured
- [ ] Test all API endpoints
- [ ] Prepare sample documents
- [ ] Close unnecessary apps
- [ ] Clean desktop
- [ ] Test screen recording software
- [ ] Prepare script/talking points
- [ ] Do a practice run
- [ ] Check audio levels
- [ ] Ensure good lighting (if showing face)

---

## 🎬 Recording Commands

### Start Recording:
```bash
# Mac: QuickTime
# File → New Screen Recording

# Or use OBS Studio
# Settings → Output → Recording Quality: High
```

### During Recording:
- Speak clearly and slowly
- Pause between sections
- Show, don't just tell
- Highlight important parts
- Use cursor to guide attention

### After Recording:
- Trim unnecessary parts
- Add title slides
- Add background music
- Add captions
- Export in 1080p
- Upload to YouTube/Drive

---

## 📤 Sharing Your Demo

### Video Platforms:
- **YouTube** (Unlisted) - Best for sharing
- **Google Drive** - Easy access
- **Loom** - Quick and simple

### Include in Submission:
- Video link
- GitHub repo link
- README with setup instructions
- Architecture diagram
- API documentation link

---

## 🎉 You're Ready!

Follow this guide step-by-step, and you'll have an impressive demo video that showcases all the features of Awaaz!

Good luck! 🚀
