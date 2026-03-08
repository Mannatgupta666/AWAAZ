"""
Document Upload API Route
Handles document upload, OCR, and verification
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import os
import sys
sys.path.append('..')
from services.ocr_service import OCRService
from services.pdf_generator import PDFGenerator
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize services with config
ocr_config = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
    's3_bucket_name': os.getenv('AWAAZ_DOCUMENTS_BUCKET'),
    'numeric_tolerance': 0.1,
    'text_similarity_threshold': 0.8
}

pdf_config = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
    's3_bucket_name': os.getenv('AWAAZ_GENERATED_BUCKET'),
    'template_directory': './templates',
    'pdf_output_directory': './output',
    'use_templates': False
}

ocr_service = OCRService(ocr_config)
pdf_generator = PDFGenerator(pdf_config)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DocumentVerificationResponse(BaseModel):
    document_type: str
    verified: bool
    name: Optional[str] = None
    document_number: Optional[str] = None
    dob: Optional[str] = None  # Date of Birth
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    errors: Optional[list] = None
    clarity_score: Optional[float] = None

class AffidavitRequest(BaseModel):
    user_name: str
    father_name: str
    address: str
    purpose: str
    language: str = "en"

@router.post("/upload-document", response_model=DocumentVerificationResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "auto",
    expected_name: Optional[str] = None
):
    """
    Upload and verify document using OCR
    Supports: Aadhaar, PAN, Voter ID, Driving License, etc.
    """
    try:
        print(f"Received file: {file.filename}, type: {document_type}")
        
        # Read file content
        content = await file.read()
        print(f"File size: {len(content)} bytes")
        
        # Process document using OCR service
        print("Calling OCR service...")
        ocr_result = ocr_service.process_document(content, document_type)
        print(f"OCR result status: {ocr_result.get('status')}")
        
        if ocr_result['status'] == 'error':
            error_msg = ocr_result.get('error_message', 'Unknown OCR error')
            print(f"OCR error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        extracted_data = ocr_result.get('extracted_data', {})
        print(f"Extracted data: {extracted_data}")
        
        # Calculate average confidence score (as decimal 0-1, not percentage)
        confidence_scores = ocr_result.get('confidence_scores', {})
        if confidence_scores:
            scores = [v/100 if v > 1 else v for v in confidence_scores.values() if isinstance(v, (int, float))]
            avg_confidence = sum(scores) / len(scores) if scores else 0.97
        else:
            avg_confidence = 0.97  # Default for mock OCR (97%)
        
        return DocumentVerificationResponse(
            document_type=document_type,
            verified=ocr_result['status'] == 'success',
            name=extracted_data.get('name'),
            document_number=extracted_data.get('aadhaar_number') or extracted_data.get('document_number'),
            dob=extracted_data.get('dob'),
            clarity_score=avg_confidence,
            errors=[]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Document upload failed: {str(e) or 'Unknown error'}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

@router.post("/generate-affidavit")
async def generate_affidavit(request: AffidavitRequest):
    """
    Generate affidavit PDF for missing documents
    """
    try:
        # Prepare user data for PDF generation
        user_data = {
            'user_id': 'user_' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'name': request.user_name,
            'father_name': request.father_name,
            'address': request.address,
            'scheme': request.purpose,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Generate PDF using the correct method
        result = pdf_generator.generate_pdf(user_data, 'affidavit')
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['error_message'])
        
        # Extract just the filename from the path
        pdf_filename = os.path.basename(result['pdf_path'])
        
        return {
            "success": True,
            "pdf_path": result['pdf_path'],
            "pdf_filename": pdf_filename,
            "s3_url": result.get('s3_url'),
            "message": "Affidavit generated successfully",
            "next_steps": [
                "Print the affidavit",
                "Sign in front of notary",
                "Attach with application"
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Affidavit generation failed: {str(e)}")

@router.get("/download-pdf/{filename}")
async def download_pdf(filename: str):
    """
    Serve PDF file for download/viewing
    """
    from fastapi.responses import FileResponse
    
    try:
        # Construct file path
        file_path = os.path.join("output", filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="PDF file not found")
        
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve PDF: {str(e)}")

@router.post("/generate-application-form")
async def generate_application_form(scheme_name: str, user_data: Dict):
    """
    Generate pre-filled application form for a scheme
    """
    try:
        # Generate application form PDF
        pdf_path = pdf_generator.generate_application_form(
            scheme_name=scheme_name,
            user_data=user_data
        )
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "scheme": scheme_name,
            "message": "Application form generated successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Form generation failed: {str(e)}")

@router.get("/document-requirements/{scheme_name}")
async def get_document_requirements(scheme_name: str):
    """
    Get list of required documents for a specific scheme
    """
    try:
        # Document requirements mapping
        requirements = {
            "PM Kisan": ["Aadhaar Card", "Bank Passbook", "Land Records"],
            "Ayushman Bharat": ["Aadhaar Card", "Ration Card", "Income Certificate"],
            "Domicile Certificate": ["Aadhaar Card", "PAN Card", "Address Proof", "Photograph"],
            "Ration Card": ["Aadhaar Card", "Address Proof", "Income Certificate", "Photograph"]
        }
        
        docs = requirements.get(scheme_name, [])
        
        return {
            "scheme": scheme_name,
            "required_documents": docs,
            "total_count": len(docs)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requirements: {str(e)}")

@router.post("/check-document-status")
async def check_document_status(user_id: str, document_type: str):
    """
    Check if user has already uploaded a specific document
    """
    try:
        # This would query the database in production
        # For now, return mock response
        return {
            "user_id": user_id,
            "document_type": document_type,
            "uploaded": False,
            "verified": False,
            "upload_date": None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
