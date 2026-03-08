# Awaaz - AI Government Scheme Assistant 🇮🇳

AI-powered assistant that helps Indian citizens find and apply for government schemes through voice and text interaction.

## 🎯 Features

- 💬 WhatsApp-style chat interface
- 🎤 Voice interaction in Indian languages (via Bhashini)
- 🔍 AI-powered scheme eligibility detection (Amazon Bedrock)
- 📄 Document verification using OCR (Amazon Textract)
- 📝 Automatic form/affidavit generation
- 🌐 Multi-language support

## 🏗️ Architecture

```
User → Frontend (HTML/JS) → Backend (FastAPI) → AWS Services
                                                  ├── Bedrock (AI)
                                                  ├── Textract (OCR)
                                                  └── S3 (Storage)
```

## 📁 Project Structure

```
AWAAZ/
├── frontend/              # HTML, CSS, JavaScript UI
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── backend/               # FastAPI backend
│   ├── routes/            # API endpoints
│   │   ├── chat.py        # Chat API
│   │   ├── speech.py      # Voice processing
│   │   └── upload.py      # Document upload
│   │
│   ├── services/          # Business logic
│   │   ├── scheme_engine.py    # AI scheme matching
│   │   ├── ocr_service.py      # Document OCR
│   │   └── pdf_generator.py    # PDF generation
│   │
│   ├── config/            # Configuration
│   │   └── aws_config.py  # AWS client setup
│   │
│   ├── main.py            # FastAPI app
│   └── requirements.txt   # Python dependencies
│
├── database/              # SQLite database
│   └── schemes.db
│
└── services/              # Additional services
    └── service_scheme.py
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with credits
- Bhashini API credentials (optional)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AWAAZ
```

2. **Backend Setup**
```bash
cd backend

# Create environment file
cp .env.example .env

# Edit .env and add your AWS credentials
nano .env

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

3. **Frontend Setup**
```bash
cd frontend

# Open index.html in browser
# Or use Live Server extension in VS Code
```

Frontend runs on: `http://localhost:5500` (or just open the HTML file)

## 🔐 Environment Variables

Create a `.env` file in the `backend/` folder:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# S3 Buckets
AWAAZ_DOCUMENTS_BUCKET=awaaz-docs-123
AWAAZ_SCHEMES_BUCKET=awaaz-schemes-123
AWAAZ_GENERATED_BUCKET=awaaz-generated-123

# Bedrock
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_REGION=us-east-1

# Bhashini (Optional)
BHASHINI_API_KEY=your_key
BHASHINI_USER_ID=your_user_id
```

**⚠️ NEVER commit the `.env` file to GitHub!**

## 📡 API Endpoints

### Chat API
```http
POST /api/chat
Content-Type: application/json

{
  "message": "I am a farmer",
  "language": "hi"
}
```

### Speech to Text
```http
POST /api/speech-to-text
Content-Type: multipart/form-data

file: <audio_file>
language: hi
```

### Text to Speech
```http
POST /api/text-to-speech
Content-Type: application/json

{
  "text": "Namaste",
  "language": "hi",
  "gender": "female"
}
```

### Upload Document
```http
POST /api/upload-document
Content-Type: multipart/form-data

file: <image_file>
document_type: aadhaar
expected_name: Ramesh Kumar
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI (Python) |
| AI Engine | Amazon Bedrock (Claude) |
| OCR | Amazon Textract |
| Storage | Amazon S3 |
| Database | SQLite |
| Voice | Bhashini API |
| PDF Generation | ReportLab |
| Cloud | AWS |

## 💰 AWS Services Used

- **Amazon Bedrock**: AI-powered scheme matching and conversation
- **Amazon Textract**: Document OCR (Aadhaar, PAN, etc.)
- **Amazon S3**: Document and PDF storage
- **Amazon DynamoDB**: User profiles (optional)

**Estimated Cost**: ~$50-60/month with $100 credits = 2 months free!

## 👥 Team Setup

See [TEAM_SETUP_GUIDE.md](TEAM_SETUP_GUIDE.md) for detailed instructions on:
- Setting up your development environment
- Getting AWS credentials
- Git workflow
- Troubleshooting common issues

## 🔒 Security

- AWS credentials stored in `.env` (not committed to git)
- `.gitignore` prevents sensitive files from being pushed
- S3 buckets with proper access controls
- Document encryption at rest

## 📚 Documentation

- [AWS Credits Usage Guide](AWS_CREDITS_USAGE_GUIDE.md)
- [Security Instructions](SECURITY_INSTRUCTIONS.md)
- [Team Setup Guide](TEAM_SETUP_GUIDE.md)

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure you're in the backend folder
cd backend

# Install dependencies
pip install -r requirements.txt

# Check if .env file exists
ls -la .env
```

### AWS connection errors
- Verify credentials in `.env` file
- Check if Bedrock model access is enabled in AWS Console
- Ensure S3 buckets are created

### Frontend can't connect to backend
- Make sure backend is running on `http://localhost:8000`
- Check CORS settings in `main.py`
- Verify API endpoint URLs in frontend code

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the team setup guide
3. Contact the team lead

## 📄 License

This project is for educational purposes (AI for Bharat Hackathon).

---

Made with ❤️ for Indian citizens
