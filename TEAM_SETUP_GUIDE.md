# Awaaz Project - Team Setup Guide

## 🚀 Quick Start for Team Members

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/awaaz-project.git
cd awaaz-project
```

### 2. Setup Based on Your Role

#### **Frontend Developer:**

```bash
cd frontend
# Open index.html in your browser
# Or use Live Server in VS Code
```

That's it! The frontend will connect to `http://localhost:8000` for the backend.

#### **Backend Developer:**

```bash
cd backend

# Create environment file
cp .env.example .env

# Edit .env and add AWS credentials (ask team lead)
nano .env

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`

### 3. Get AWS Credentials

**Ask the team lead for:**
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

**Add them to your `.env` file:**

```env
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

**⚠️ NEVER commit the `.env` file to GitHub!**

---

## 🔗 API Endpoints

### Chat API
```
POST http://localhost:8000/api/chat
Body: {"message": "I am a farmer", "language": "hi"}
```

### Speech to Text
```
POST http://localhost:8000/api/speech-to-text
Body: FormData with audio file
```

### Text to Speech
```
POST http://localhost:8000/api/text-to-speech
Body: {"text": "Hello", "language": "hi"}
```

### Upload Document
```
POST http://localhost:8000/api/upload-document
Body: FormData with image file
```

---

## 📁 Project Structure

```
awaaz-project/
├── frontend/           ← Frontend team works here
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/            ← Backend team works here
│   ├── routes/         ← API endpoints
│   ├── services/       ← Business logic
│   ├── config/         ← AWS configuration
│   └── main.py         ← FastAPI app
│
└── README.md
```

---

## 🔄 Git Workflow

### Before Starting Work:
```bash
git pull
```

### After Making Changes:
```bash
git add .
git commit -m "Describe your changes"
git push
```

### If There's a Conflict:
```bash
git pull
# Resolve conflicts in VS Code
git add .
git commit -m "Resolved conflicts"
git push
```

---

## 🆘 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Connection refused to localhost:8000"
Make sure backend is running:
```bash
cd backend
uvicorn main:app --reload
```

### "AWS credentials not found"
Make sure you created `.env` file in `backend/` folder with valid credentials.

---

## 👥 Team Roles

- **Member 1 (Frontend):** HTML, CSS, JavaScript UI
- **Member 2 (Backend - You):** FastAPI routes, AWS integration
- **Member 3 (OCR):** Document verification logic

---

## 📞 Contact

If you have issues, contact the team lead or check the main README.md
