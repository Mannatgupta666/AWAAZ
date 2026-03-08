"""
Awaaz - AI Government Scheme Assistant
FastAPI Backend Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes import chat, speech, upload

# Initialize FastAPI app
app = FastAPI(
    title="Awaaz API",
    description="AI-powered government scheme assistant for India",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(speech.router, prefix="/api", tags=["Speech"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Awaaz API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "speech_to_text": "/api/speech-to-text",
            "text_to_speech": "/api/text-to-speech",
            "upload_document": "/api/upload-document",
            "generate_affidavit": "/api/generate-affidavit",
            "schemes": "/api/schemes"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "aws_configured": bool(os.getenv("AWS_ACCESS_KEY_ID")),
        "bhashini_configured": bool(os.getenv("BHASHINI_API_KEY"))
    }

# API documentation
@app.get("/api/info")
async def api_info():
    return {
        "name": "Awaaz API",
        "description": "AI-powered government scheme assistant",
        "features": [
            "Voice interaction in Indian languages",
            "AI-powered scheme matching",
            "Document verification with OCR",
            "Automatic form generation"
        ],
        "tech_stack": {
            "backend": "FastAPI",
            "ai": "Amazon Bedrock",
            "ocr": "Amazon Textract",
            "storage": "Amazon S3",
            "voice": "Bhashini API"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
