# 🎤 Bhashini API Setup Guide (10 Minutes)

## What is Bhashini?

Bhashini is a **FREE** Government of India initiative for Indian language AI services:
- Speech-to-Text (ASR) in 22+ Indian languages
- Text-to-Speech (TTS) with natural voices
- Translation between Indian languages
- **100% FREE for developers**

---

## 🚀 Step-by-Step Registration

### Step 1: Go to Bhashini Website

Open this link in your browser:
```
https://bhashini.gov.in/ulca/user/register
```

### Step 2: Fill Registration Form

**Required Information:**
- Full Name: Your name
- Email: Your email address
- Phone: Your mobile number
- Organization: Your college/company name
- Role: Select "Developer" or "Student"
- Use Case: "Government scheme assistance for citizens"

**Click:** "Register"

### Step 3: Verify Email

1. Check your email inbox
2. Click the verification link
3. Your account is now active!

### Step 4: Login

Go to: https://bhashini.gov.in/ulca/user/login
- Enter your email and password
- Click "Login"

### Step 5: Get API Credentials

1. After login, go to **"My Profile"** or **"API Keys"**
2. Click **"Generate API Key"**
3. You'll see:
   - **API Key** (long string)
   - **User ID** (your identifier)
4. **Copy both** - you'll need them!

---

## 🔐 Add Credentials to Your App

### Open your .env file:

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
nano .env
```

### Add these lines at the bottom:

```env
# Bhashini API (Voice Processing)
BHASHINI_API_KEY=your_api_key_here
BHASHINI_USER_ID=your_user_id_here
```

**Replace:**
- `your_api_key_here` with your actual API key
- `your_user_id_here` with your actual user ID

**Save:** Press `Ctrl + X`, then `Y`, then `Enter`

---

## ✅ Test Voice Features

### Restart your backend:

```bash
# Stop the current backend (Ctrl + C)
# Start again
python3 -m uvicorn main:app --reload
```

### Test Speech-to-Text:

Open your test page and you'll see voice features working!

Or test with curl:

```bash
# Test text-to-speech
curl -X POST http://localhost:8000/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Namaste, main Awaaz hoon",
    "language": "hi",
    "gender": "female"
  }' \
  --output test_speech.wav

# Play the audio
open test_speech.wav
```

---

## 🎯 Supported Languages

Bhashini supports these Indian languages:

| Language | Code | Language | Code |
|----------|------|----------|------|
| Hindi | `hi` | Tamil | `ta` |
| Bengali | `bn` | Telugu | `te` |
| Marathi | `mr` | Kannada | `kn` |
| Gujarati | `gu` | Malayalam | `ml` |
| Punjabi | `pa` | Odia | `or` |
| Urdu | `ur` | Assamese | `as` |

And many more!

---

## 🎥 For Your Demo Video

Once Bhashini is set up, you can show:

1. **Voice Input:**
   - User speaks in Hindi: "Mujhe kisan yojana chahiye"
   - System transcribes to text
   - AI responds with scheme information

2. **Voice Output:**
   - System reads response in Hindi
   - Natural-sounding voice
   - Multiple language support

3. **Translation:**
   - User speaks in Tamil
   - System translates to Hindi
   - Responds in Tamil

---

## 🐛 Troubleshooting

### "API Key Invalid"
- Make sure you copied the entire key
- No extra spaces before/after
- Check if key is active in Bhashini dashboard

### "User ID not found"
- Verify User ID is correct
- Check if account is verified (check email)

### "Service unavailable"
- Bhashini servers might be down temporarily
- Try again in a few minutes
- Check status: https://bhashini.gov.in/status

---

## 📊 API Limits (All FREE!)

- **Requests:** Unlimited for development
- **Languages:** 22+ Indian languages
- **Quality:** Production-ready
- **Support:** Community forums

---

## 🔗 Useful Links

- **Registration:** https://bhashini.gov.in/ulca/user/register
- **Login:** https://bhashini.gov.in/ulca/user/login
- **Documentation:** https://bhashini.gitbook.io/bhashini-apis/
- **API Playground:** https://bhashini.gov.in/ulca/api-playground
- **Support:** support@bhashini.gov.in

---

## ✅ Checklist

- [ ] Registered on Bhashini website
- [ ] Verified email
- [ ] Generated API key
- [ ] Copied API key and User ID
- [ ] Added to `.env` file
- [ ] Restarted backend
- [ ] Tested voice features
- [ ] Ready for demo!

---

## 🎉 You're Done!

Your Awaaz app now has:
- ✅ AI scheme matching (Bedrock)
- ✅ Document OCR (Textract)
- ✅ Voice processing (Bhashini)
- ✅ PDF generation
- ✅ Multi-language support

**Perfect for your demo video!** 🚀

---

## 💡 Demo Tips

**Show this flow:**
1. User speaks in Hindi (use microphone)
2. System transcribes to text
3. AI matches to scheme
4. System responds in Hindi voice
5. User uploads Aadhaar
6. System verifies and generates form

**This showcases:**
- Voice-first interface ✅
- AI intelligence ✅
- Document processing ✅
- Multi-language support ✅
- End-to-end workflow ✅

---

**Need help? The Bhashini team is very responsive to developers working on public good projects!**
