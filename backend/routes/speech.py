"""
Speech API Route
Handles voice input/output using Bhashini API
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import os
import io
from typing import Optional

router = APIRouter()

# Bhashini API Configuration
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY", "")
BHASHINI_USER_ID = os.getenv("BHASHINI_USER_ID", "")
BHASHINI_BASE_URL = "https://dhruva-api.bhashini.gov.in/services"

class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "hi"  # Default to Hindi
    gender: str = "female"

class SpeechToTextResponse(BaseModel):
    text: str
    language: str
    confidence: Optional[float] = None

@router.post("/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text(audio_file: UploadFile = File(...), language: str = "hi"):
    """
    Convert speech to text using Bhashini ASR
    """
    try:
        # Read audio file
        audio_content = await audio_file.read()
        
        # Prepare Bhashini ASR request
        asr_url = f"{BHASHINI_BASE_URL}/inference/pipeline"
        
        headers = {
            "Authorization": f"Bearer {BHASHINI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": language
                        },
                        "serviceId": "ai4bharat/conformer-hi-gpu--t4",
                        "audioFormat": "wav",
                        "samplingRate": 16000
                    }
                }
            ],
            "inputData": {
                "audio": [
                    {
                        "audioContent": audio_content.hex()
                    }
                ]
            }
        }
        
        # Call Bhashini API
        response = requests.post(asr_url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Bhashini ASR failed")
        
        result = response.json()
        transcribed_text = result.get("pipelineResponse", [{}])[0].get("output", [{}])[0].get("source", "")
        
        return SpeechToTextResponse(
            text=transcribed_text,
            language=language,
            confidence=0.95
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {str(e)}")

@router.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech using Bhashini TTS
    Returns audio file
    """
    try:
        # Prepare Bhashini TTS request
        tts_url = f"{BHASHINI_BASE_URL}/inference/pipeline"
        
        headers = {
            "Authorization": f"Bearer {BHASHINI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": request.language
                        },
                        "serviceId": "ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",
                        "gender": request.gender,
                        "samplingRate": 22050
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": request.text
                    }
                ]
            }
        }
        
        # Call Bhashini API
        response = requests.post(tts_url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Bhashini TTS failed")
        
        result = response.json()
        audio_content = result.get("pipelineResponse", [{}])[0].get("audio", [{}])[0].get("audioContent", "")
        
        # Convert hex to bytes
        audio_bytes = bytes.fromhex(audio_content)
        
        # Return as streaming audio
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {str(e)}")

@router.post("/translate")
async def translate_text(text: str, source_lang: str, target_lang: str):
    """
    Translate text between Indian languages using Bhashini
    """
    try:
        translation_url = f"{BHASHINI_BASE_URL}/inference/pipeline"
        
        headers = {
            "Authorization": f"Bearer {BHASHINI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
                        },
                        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ]
            }
        }
        
        response = requests.post(translation_url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Translation failed")
        
        result = response.json()
        translated_text = result.get("pipelineResponse", [{}])[0].get("output", [{}])[0].get("target", "")
        
        return {
            "original": text,
            "translated": translated_text,
            "source_language": source_lang,
            "target_language": target_lang
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
