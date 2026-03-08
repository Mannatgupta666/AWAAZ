"""
Chat API Route
Handles text-based conversation and scheme matching
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
sys.path.append('..')
from services.scheme_engine import SchemeEngine

router = APIRouter()
scheme_engine = SchemeEngine()

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    schemes: List[str]
    next_step: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user message and return scheme recommendations
    """
    try:
        # Extract user information from message
        user_data = scheme_engine.extract_user_info(request.message, request.language)
        
        # Match eligible schemes
        matched_schemes = scheme_engine.match_schemes(user_data)
        
        # Generate conversational response
        reply = scheme_engine.generate_response(
            user_data=user_data,
            schemes=matched_schemes,
            language=request.language
        )
        
        # Determine next step
        next_step = None
        if matched_schemes:
            next_step = "document_upload"
        
        return ChatResponse(
            reply=reply,
            schemes=[s["name"] for s in matched_schemes],
            next_step=next_step
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@router.get("/schemes")
async def get_all_schemes():
    """
    Return list of all available schemes
    """
    try:
        schemes = scheme_engine.get_all_schemes()
        return {"schemes": schemes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch schemes: {str(e)}")

@router.post("/schemes/check-eligibility")
async def check_eligibility(user_data: dict):
    """
    Check eligibility for specific schemes based on user data
    """
    try:
        eligible_schemes = scheme_engine.match_schemes(user_data)
        return {
            "eligible": len(eligible_schemes) > 0,
            "schemes": eligible_schemes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eligibility check failed: {str(e)}")
