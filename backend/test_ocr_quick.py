"""
Quick OCR test with existing image
"""
import sys
from services.ocr_service import OCRService
from config.aws_config import aws_config

# Initialize OCR service
config = {
    'aws_access_key_id': aws_config.aws_access_key,
    'aws_secret_access_key': aws_config.aws_secret_key,
    'aws_region': aws_config.aws_region,
    's3_bucket_name': aws_config.documents_bucket,
    'numeric_tolerance': 0.1,
    'text_similarity_threshold': 0.8
}

ocr_service = OCRService(config)

# Test with uploaded image
image_path = 'uploads/1772943717.195864_awaaz-architecture.png'

print("Testing OCR with architecture diagram...")
print("=" * 60)

result = ocr_service.process_document(image_path, 'aadhaar')

print(f"Status: {result['status']}")
print(f"\nExtracted Text:")
print("-" * 60)

if result['status'] == 'success':
    print(f"Extracted Data: {result['extracted_data']}")
    print(f"\nS3 URL: {result['s3_url']}")
    print(f"\nConfidence Scores (top 5):")
    for i, (text, score) in enumerate(list(result['confidence_scores'].items())[:5]):
        print(f"  {i+1}. '{text}': {score:.1f}%")
else:
    print(f"Error: {result['error_message']}")

print("=" * 60)
print("\nNote: This is testing with an architecture diagram.")
print("For best results, upload a document image (Aadhaar, certificate, etc.)")
