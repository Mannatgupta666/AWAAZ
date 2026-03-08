"""
Quick test to check if AWS Textract is activated
"""
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def test_textract():
    """Test if Textract is activated"""
    try:
        client = boto3.client(
            'textract',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        # Try a simple test with minimal data
        test_image = b'\xff\xd8\xff\xe0\x00\x10JFIF'  # Minimal JPEG header
        
        print("Testing Textract activation...")
        response = client.detect_document_text(
            Document={'Bytes': test_image}
        )
        
        print("✅ SUCCESS! Textract is activated and working!")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Textract Status: {error_str}")
        
        if "SubscriptionRequiredException" in error_str:
            print("\n⏳ Textract not yet activated. This is normal.")
            print("   Wait 5-30 minutes after adding payment method.")
            print("   Your mock OCR fallback is working perfectly for demo!")
        elif "InvalidImageException" in error_str:
            print("\n✅ GOOD NEWS! Textract is activated!")
            print("   (The error is just from our test image, not a real issue)")
            return True
        else:
            print(f"\n⚠️  Unexpected error: {error_str}")
        
        return False

if __name__ == "__main__":
    test_textract()
