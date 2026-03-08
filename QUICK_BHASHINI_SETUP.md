# ⚡ Quick Bhashini Setup (5 Minutes)

## 1️⃣ Register (2 minutes)

**Go to:** https://bhashini.gov.in/ulca/user/register

**Fill:**
- Name: Your name
- Email: Your email
- Phone: Your number
- Organization: Your college
- Role: Developer
- Use Case: "Government scheme assistance"

**Click:** Register → Verify email

---

## 2️⃣ Get API Key (1 minute)

**Login:** https://bhashini.gov.in/ulca/user/login

**Go to:** My Profile → API Keys → Generate

**Copy:**
- API Key
- User ID

---

## 3️⃣ Add to .env (1 minute)

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
nano .env
```

**Add at bottom:**
```env
BHASHINI_API_KEY=paste_your_key_here
BHASHINI_USER_ID=paste_your_id_here
```

**Save:** Ctrl+X → Y → Enter

---

## 4️⃣ Restart Backend (30 seconds)

```bash
# Stop: Ctrl+C
# Start:
python3 -m uvicorn main:app --reload
```

---

## 5️⃣ Test (30 seconds)

Refresh test page → Voice features now work!

---

## ✅ Done!

Voice processing in 22+ Indian languages is now active! 🎤

---

## 🆘 Issues?

**Can't register?**
- Use different email
- Check spam folder for verification

**API key not working?**
- Copy entire key (no spaces)
- Restart backend after adding to .env

**Still stuck?**
- Email: support@bhashini.gov.in
- They respond within 24 hours

---

## 🎥 For Demo

**Show:**
1. Speak in Hindi
2. System transcribes
3. AI responds
4. System speaks back

**Mention:**
"Powered by Bhashini - Government of India's free AI for Indian languages"

---

**Total time: 5 minutes | Cost: FREE | Languages: 22+ | Quality: Production-ready**
