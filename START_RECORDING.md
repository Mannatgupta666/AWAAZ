# Quick Start: Record Your Demo

## ✅ Status Check
All features tested and working! You're ready to record.

## 🎬 Recording in 3 Steps

### Step 1: Start Backend (if not running)
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 -m uvicorn main:app --reload
```
Wait for: `Application startup complete`

### Step 2: Open Test Page
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

### Step 3: Start Recording

**Mac Built-in (QuickTime):**
1. Open QuickTime Player
2. File → New Screen Recording
3. Click record, then click screen
4. Follow demo script below
5. Click Stop in menu bar when done

**Alternative (Loom - Easier):**
1. Download Loom: https://www.loom.com/
2. Click Loom icon in menu bar
3. Select "Screen Only" or "Screen + Cam"
4. Click "Start Recording"

## 📝 7-Minute Demo Script

### 0:00-0:30 | Introduction
```
"Hi! I'm presenting Awaaz - an AI-powered assistant that helps 
Indian citizens discover and apply for government schemes through 
simple conversation. Let me show you how it works."
```

### 0:30-1:00 | Show Test Page
- Show the test page interface
- Point out the 5 features we'll demo

### 1:00-2:00 | Test 1: Health Check
- Click "Check Backend Status"
- Show: Backend online, AWS configured
- Explain: "Backend is running with AWS services"

### 2:00-3:30 | Test 2: Chat API
- Type: "I am a 35 year old farmer from Punjab with 2 acres of land"
- Click "Send Message"
- Show response: "You may be eligible for PM Kisan"
- Explain: "System understands natural language and matches schemes"

### 3:30-4:00 | Test 3: Get Schemes
- Click "Fetch Schemes"
- Show: PM Kisan, Ayushman Bharat
- Explain: "Database of government schemes with eligibility criteria"

### 4:00-5:00 | Test 4: Document Upload
- Click "Choose File"
- Upload any image (Aadhaar, PAN, or any document)
- Show: OCR extraction result
- Explain: "Amazon Textract verifies documents automatically"

### 5:00-6:30 | Test 5: Generate Affidavit
- Fill in form:
  - Name: Ramesh Kumar
  - Scheme: PM Kisan
  - Age: 35
  - Occupation: Farmer
- Click "Generate PDF"
- Show success message
- Open Finder → Navigate to `backend/output/`
- Open the generated PDF
- Explain: "Automatic form generation for applications"

### 6:30-7:00 | Conclusion
```
"Awaaz makes government schemes accessible through:
- Natural language chat
- Document verification with OCR
- Automatic form generation
- Simple, user-friendly interface

Future features include voice interaction in Indian languages 
and WhatsApp integration. Thank you!"
```

## 🎯 What to Show

✅ **Show these (working):**
- Test page interface
- Health check
- Chat with scheme matching
- Scheme database
- Document upload (with any image)
- PDF generation

⚠️ **Mention but don't demo:**
- Bedrock AI (pending setup)
- Bhashini voice (pending API key)
- WhatsApp integration (future)

## 💡 Pro Tips

1. **Speak slowly and clearly**
2. **Pause between features** (1-2 seconds)
3. **Show cursor movements smoothly**
4. **If something fails, stay calm** - just say "let me try that again"
5. **Smile!** Even if they can't see you, it helps your voice sound friendly

## 🐛 Quick Fixes During Recording

**If backend stops responding:**
```bash
# In terminal, press Ctrl+C, then restart:
python3 -m uvicorn main:app --reload
```

**If test page doesn't load:**
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

**If you make a mistake:**
- Just pause, take a breath
- Say "Let me show that again"
- Continue from that point
- You can edit it out later

## 📤 After Recording

1. **Save video** as `awaaz-demo.mp4`
2. **Watch it once** to check quality
3. **Check audio** is clear
4. **Verify all features** were shown
5. **Upload** to required platform

## ⏱️ Time Management

- Introduction: 30 sec
- Each feature: 1-1.5 min
- Conclusion: 30 sec
- Total: 6-7 minutes

Don't rush! It's better to be clear and take 7 minutes than to rush through in 5.

---

## Ready? Let's Go! 🚀

1. ✅ Backend running
2. ✅ Test page open
3. ✅ Recording tool ready
4. ✅ Script reviewed

**Click record and follow the script above!**

Good luck! 🎬
