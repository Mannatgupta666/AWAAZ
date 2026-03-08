# 🍎 Mac-Specific Commands

## ⚠️ Important: Use `pip3` and `python3` on Mac

Your Mac uses `pip3` and `python3` (not `pip` and `python`).

---

## 🚀 Quick Start Commands (Mac)

### Step 1: Navigate to Project
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
```

### Step 2: Install Dependencies
```bash
pip3 install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- boto3 (AWS SDK)
- ReportLab (PDF generation)
- OpenCV (Image processing)
- And more...

### Step 3: Test AWS Connection
```bash
python3 -c "from config.aws_config import aws_config; print('✅ AWS connected!')"
```

### Step 4: Start Backend
```bash
python3 -m uvicorn main:app --reload
```

Or simply:
```bash
uvicorn main:app --reload
```

### Step 5: Test APIs (New Terminal)
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 test_api.py
```

### Step 6: Open Test Page
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

---

## 🔧 Troubleshooting

### "pip3: command not found"
Install pip3:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### "uvicorn: command not found"
Install uvicorn:
```bash
pip3 install uvicorn[standard]
```

### "Permission denied"
Use sudo:
```bash
sudo pip3 install -r requirements.txt
```

### "Module not found" errors
Make sure you're in the backend folder:
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
pip3 install -r requirements.txt
```

---

## ✅ Complete Setup Script (Copy & Paste)

```bash
# Go to backend folder
cd ~/aiforbharat\ hackathon/AWAAZ/backend

# Install all dependencies
pip3 install -r requirements.txt

# Test AWS connection (after adding credentials to .env)
python3 -c "from config.aws_config import aws_config; print('✅ AWS connected!')"

# Start the backend
python3 -m uvicorn main:app --reload
```

---

## 🎥 Demo Recording Commands

### Terminal 1: Start Backend
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 -m uvicorn main:app --reload
```

### Terminal 2: Test APIs
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 test_api.py
```

### Browser: Open Test Page
```bash
open ~/aiforbharat\ hackathon/AWAAZ/test_page.html
```

---

## 📋 Quick Reference

| Command | Mac Version |
|---------|-------------|
| `pip install` | `pip3 install` |
| `python` | `python3` |
| `pip list` | `pip3 list` |
| `python --version` | `python3 --version` |

---

## 🆘 Still Having Issues?

### Check Python Installation
```bash
python3 --version
pip3 --version
```

Should show:
```
Python 3.9.6
pip 21.x.x
```

### Reinstall pip3
```bash
python3 -m ensurepip --upgrade
```

### Use Virtual Environment (Recommended)
```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Now use pip (not pip3)
pip install -r requirements.txt

# Start backend
uvicorn main:app --reload
```

---

## ✅ You're Ready!

Use `pip3` and `python3` for all commands, and everything will work perfectly! 🚀
