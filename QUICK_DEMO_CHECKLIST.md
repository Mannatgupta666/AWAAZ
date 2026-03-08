# ✅ Quick Demo Checklist - 5 Minutes to Ready

## 🎯 Goal
Get your Awaaz app running and ready for demo video recording.

---

## ⚡ Super Quick Start (2 Commands)

### Terminal 1: Start Backend
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend && uvicorn main:app --reload
```

### Browser: Open Test Page
Drag this file into your browser:
```
~/aiforbharat hackathon/AWAAZ/test_page.html
```

**That's it!** Click the buttons to test each feature.

---

## 📋 Pre-Demo Checklist

### Before You Start:

- [ ] **AWS Credentials Setup**
  - Created `.env` file in `backend/` folder
  - Added AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
  - Enabled Bedrock model access in AWS Console

- [ ] **Dependencies Installed**
  ```bash
  cd ~/aiforbharat\ hackathon/AWAAZ/backend
  pip install -r requirements.txt
  ```

- [ ] **Backend Running**
  - Terminal shows: `INFO: Uvicorn running on http://127.0.0.1:8000`
  - Health check passes: http://localhost:8000/health

- [ ] **Test Page Working**
  - Opens in browser
  - Health status shows "Online"
  - All buttons work

---

## 🎬 Demo Recording Checklist

### Environment Setup:
- [ ] Close unnecessary apps
- [ ] Clean desktop
- [ ] Hide menu bar (optional)
- [ ] Full screen browser
- [ ] Good lighting (if showing face)
- [ ] Test microphone

### What to Show:
- [ ] **Intro** (30s): Project overview
- [ ] **Architecture** (45s): Show diagram
- [ ] **Chat Demo** (1.5min): User asks about schemes
- [ ] **Document Upload** (1.5min): OCR verification
- [ ] **Form Generation** (1min): Generate PDF
- [ ] **Code Walkthrough** (1min): Show project structure
- [ ] **AWS Integration** (45s): Show S3, Bedrock
- [ ] **Conclusion** (30s): Summary and thank you

### Recording Tools:
- [ ] Screen recorder ready (QuickTime/OBS)
- [ ] Audio levels tested
- [ ] Recording quality set to 1080p
- [ ] Save location chosen

---

## 🧪 Test Each Feature

### 1. Health Check ✅
**Test:** Click "Check Backend Status"
**Expected:** Status shows "Online", AWS configured: true

### 2. Chat API ✅
**Test:** Type "I am a farmer" → Click "Send Message"
**Expected:** AI suggests PM Kisan scheme

### 3. Get Schemes ✅
**Test:** Click "Fetch Schemes"
**Expected:** List of available schemes

### 4. Document Upload ✅
**Test:** Upload image → Click "Upload & Verify"
**Expected:** Extracted text and verification status
**Note:** Need a sample document image

### 5. Generate Affidavit ✅
**Test:** Fill form → Click "Generate PDF"
**Expected:** PDF path and success message

---

## 🎥 Recording Script (7 Minutes)

### Scene 1: Introduction (30s)
- Show project title
- Explain problem: "Helping citizens access schemes"

### Scene 2: Architecture (45s)
- Show `awaaz-architecture.png`
- Highlight: Bedrock, Textract, S3

### Scene 3: Live Demo - Chat (1.5min)
- Open test page
- Type: "I am a farmer with 2 acres"
- Show AI response
- Type: "Tell me more about PM Kisan"

### Scene 4: Document Verification (1.5min)
- Click "Upload Document"
- Upload Aadhaar image
- Show OCR results
- Highlight verification status

### Scene 5: Form Generation (1min)
- Fill affidavit form
- Click "Generate PDF"
- Show success message
- Mention S3 storage

### Scene 6: Code Walkthrough (1min)
- Show VS Code
- Highlight key files:
  - `services/ocr_service.py`
  - `services/pdf_generator.py`
  - `services/scheme_engine.py`

### Scene 7: AWS Integration (45s)
- Open AWS Console
- Show S3 buckets
- Show Bedrock access
- Mention cost optimization

### Scene 8: Conclusion (30s)
- Summary of features
- GitHub link
- Thank you

---

## 🐛 Common Issues & Fixes

### Backend won't start
```bash
# Kill existing process
lsof -i :8000
kill -9 <PID>

# Restart
uvicorn main:app --reload
```

### "AWS credentials not found"
```bash
# Check .env file exists
ls -la backend/.env

# If not, create it
cd backend
cp .env.example .env
nano .env
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### Test page shows "Offline"
- Make sure backend is running
- Check http://localhost:8000/health in browser
- Look for errors in terminal

---

## 📊 Sample Demo Data

### User Profile 1: Farmer
```
Message: "I am a farmer with 2 acres of land in Uttar Pradesh"
Expected Scheme: PM Kisan
```

### User Profile 2: Student
```
Message: "I am a 20-year-old SC category student"
Expected Scheme: Scholarship schemes
```

### User Profile 3: Senior Citizen
```
Message: "I am 65 years old with no income"
Expected Scheme: Old age pension
```

---

## ✅ Final Checklist Before Recording

- [ ] Backend running smoothly
- [ ] All API tests pass
- [ ] Test page works
- [ ] Sample documents ready
- [ ] Screen recorder tested
- [ ] Audio tested
- [ ] Script prepared
- [ ] Desktop clean
- [ ] Apps closed
- [ ] Ready to record!

---

## 🎉 You're Ready!

**Start recording and follow the script in DEMO_GUIDE.md**

Good luck with your demo! 🚀

---

## 📞 Quick Reference

**Backend URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs
**Test Page:** file:///.../AWAAZ/test_page.html

**Start Backend:**
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
uvicorn main:app --reload
```

**Test APIs:**
```bash
python test_api.py
```
