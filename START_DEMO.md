# 🚀 Quick Start - Run Demo in 2 Minutes

## Step 1: Open Terminal

Press `Cmd + Space`, type "Terminal", press Enter

## Step 2: Navigate to Project

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
```

## Step 3: Start Backend

```bash
uvicorn main:app --reload
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ Backend is running!

## Step 4: Test the API

**Open a new terminal tab** (`Cmd + T`) and run:

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python test_api.py
```

This will test all endpoints automatically.

## Step 5: Open Test Page

**In your browser, open:**
```
file:///Users/shagunbhatia30/aiforbharat%20hackathon/AWAAZ/test_page.html
```

Or just drag `test_page.html` into your browser.

## Step 6: Test Each Feature

On the test page, click each button:

1. ✅ Check Backend Status
2. ✅ Send Message (Chat API)
3. ✅ Fetch Schemes
4. ✅ Upload Document (need a sample image)
5. ✅ Generate Affidavit

---

## 🎥 Ready to Record?

Once all tests pass, you're ready to record your demo!

Follow the **DEMO_GUIDE.md** for the complete recording script.

---

## ⚠️ Troubleshooting

### "Connection refused"
Backend is not running. Go back to Step 3.

### "AWS credentials not found"
Create `.env` file:
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
cp .env.example .env
nano .env
# Add your AWS credentials
```

### "Module not found"
Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📞 Quick Commands

**Start backend:**
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend && uvicorn main:app --reload
```

**Test API:**
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend && python test_api.py
```

**Open test page:**
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

---

## ✅ Checklist

- [ ] Backend running (http://localhost:8000)
- [ ] Test page opens (test_page.html)
- [ ] Health check passes
- [ ] Chat API works
- [ ] Schemes API works
- [ ] Ready to record demo!

---

**You're all set! 🎉**
