# How to Record Your Demo Video

## Recording Tools (Mac)

**Option 1: QuickTime (Built-in, Free)**
1. Open QuickTime Player
2. File → New Screen Recording
3. Click record button
4. Click anywhere to record full screen, or drag to select area
5. Click Stop button in menu bar when done
6. File → Save

**Option 2: OBS Studio (Free, Professional)**
- Download: https://obsproject.com/
- Better quality, more control
- Can add webcam overlay

**Option 3: Loom (Free, Easy)**
- Download: https://www.loom.com/
- Records screen + webcam
- Automatically uploads and shares

## Before Recording Checklist

### 1. Start Backend
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 -m uvicorn main:app --reload
```
Wait for: `Application startup complete`

### 2. Open Test Page
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

### 3. Prepare Test Data
Have these ready:
- Test message: "I am a 35 year old farmer from Punjab"
- Test image: Any document image (Aadhaar, PAN, etc.)
- User details for affidavit

### 4. Clean Up Desktop
- Close unnecessary windows
- Hide personal information
- Clear browser history if needed

### 5. Prepare Your Script
Read through DEMO_GUIDE.md

## Recording Script (7 Minutes)

### Introduction (30 seconds)
```
"Hello! I'm presenting Awaaz - an AI-powered government scheme 
assistant for Indian citizens. Awaaz helps people discover and 
apply for government schemes through simple conversation."
```

### Demo Flow (6 minutes)

**1. Show Architecture (30 sec)**
- Open `awaaz-architecture.png`
- Explain: Frontend → Backend → AWS Services

**2. Test Health Check (30 sec)**
- Click "Check Backend Status"
- Show: Backend online, AWS configured

**3. Test Chat API (1 min)**
- Type: "I am a 35 year old farmer from Punjab with 2 acres of land"
- Click "Send Message"
- Show: AI matches PM Kisan scheme
- Explain: System understands natural language

**4. Show All Schemes (30 sec)**
- Click "Fetch Schemes"
- Show: PM Kisan, Ayushman Bharat, etc.
- Explain: Database of government schemes

**5. Test Document Upload (1 min)**
- Upload a document image
- Show: OCR extracts text
- Explain: Amazon Textract verifies documents

**6. Generate Affidavit (1 min)**
- Fill in user details
- Click "Generate PDF"
- Show: PDF created successfully
- Open the PDF from `backend/output/`
- Explain: Automatic form generation

**7. Show Code (1 min)**
- Open VS Code
- Show `scheme_engine.py` - AI matching logic
- Show `routes/chat.py` - API endpoints
- Explain: FastAPI backend with AWS integration

### Conclusion (30 seconds)
```
"Awaaz makes government schemes accessible to everyone through:
- Natural language understanding
- Multi-language support (future)
- Voice interaction (future)
- Automatic document verification
- Simple, WhatsApp-style interface

Thank you!"
```

## Recording Tips

### Audio
- Use headphones with mic or AirPods
- Record in quiet room
- Speak clearly and not too fast
- Pause between sections

### Video
- Record in 1080p (1920x1080)
- Use full screen or specific window
- Keep cursor movements smooth
- Don't rush - take your time

### Editing
- Trim beginning/end
- Cut out mistakes
- Add title slide (optional)
- Export as MP4

## Quick Recording Commands

### Start Everything
```bash
# Terminal 1: Start backend
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 -m uvicorn main:app --reload

# Terminal 2: Open test page
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html

# Open architecture diagram
open ~/aiforbharat\ hackathon/generated-diagrams/awaaz-architecture.png
```

### During Recording
1. Start screen recording
2. Follow demo script
3. Show each feature working
4. Explain what's happening
5. Stop recording

### After Recording
1. Save video file
2. Watch it once to check quality
3. Re-record if needed
4. Upload to required platform

## What to Highlight

✅ **Working Features:**
- Chat API with scheme matching
- Document OCR (Amazon Textract)
- PDF generation
- RESTful API design
- AWS integration
- Database of schemes

⚠️ **Future Features (mention but don't demo):**
- Bedrock AI (pending payment setup)
- Bhashini voice (pending API key)
- WhatsApp integration
- Multi-language support

## Common Issues During Recording

**Backend not responding:**
```bash
# Restart backend
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 -m uvicorn main:app --reload
```

**Test page not loading:**
```bash
# Reopen test page
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

**PDF not generating:**
- Check `backend/output/` folder exists
- Verify all fields are filled

## Video Specifications

**Format:** MP4 (H.264)
**Resolution:** 1920x1080 (1080p) or 1280x720 (720p)
**Duration:** 5-7 minutes
**File Size:** Under 500MB
**Audio:** Clear, no background noise

## Export Settings (QuickTime)

1. File → Export As → 1080p
2. Save to Desktop
3. Rename: `awaaz-demo-[your-name].mp4`

## Upload Checklist

- [ ] Video recorded and saved
- [ ] Audio is clear
- [ ] All features demonstrated
- [ ] No personal information visible
- [ ] File size under limit
- [ ] Correct format (MP4)
- [ ] Ready to upload

---

**Good luck with your demo! 🎬**

Your app works great - just show what you've built with confidence!
