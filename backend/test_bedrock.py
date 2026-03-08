"""
Test script to verify Amazon Bedrock AI is working
"""
import sys
import json
from services.scheme_engine import SchemeEngine
from config.aws_config import aws_config

def test_bedrock_connection():
    """Test if Bedrock client is initialized"""
    print("=" * 60)
    print("TESTING BEDROCK CONNECTION")
    print("=" * 60)
    
    try:
        print(f"✓ Bedrock client initialized: {aws_config.bedrock_client is not None}")
        print(f"✓ Model ID: {aws_config.bedrock_model_id}")
        print(f"✓ Region: {aws_config.bedrock_region}")
        return True
    except Exception as e:
        print(f"✗ Bedrock initialization failed: {str(e)}")
        return False

def test_user_info_extraction():
    """Test AI-powered user info extraction"""
    print("\n" + "=" * 60)
    print("TESTING USER INFO EXTRACTION (AI)")
    print("=" * 60)
    
    engine = SchemeEngine()
    test_message = "I am a 35 year old farmer from Punjab with 2 acres of land and annual income of 1.5 lakhs"
    
    print(f"\nTest message: {test_message}")
    print("\nCalling Bedrock AI to extract user info...")
    
    try:
        user_data = engine.extract_user_info(test_message)
        print("\n✓ Extraction successful!")
        print(f"Extracted data: {json.dumps(user_data, indent=2)}")
        
        # Check if it's using AI or fallback
        if len(user_data) > 2:
            print("\n✓ BEDROCK AI IS WORKING! (Rich data extracted)")
            return True
        else:
            print("\n⚠ Using fallback extraction (limited data)")
            return False
            
    except Exception as e:
        print(f"\n✗ Extraction failed: {str(e)}")
        return False

def test_scheme_matching():
    """Test AI-powered scheme matching"""
    print("\n" + "=" * 60)
    print("TESTING SCHEME MATCHING (AI)")
    print("=" * 60)
    
    engine = SchemeEngine()
    test_user_data = {
        "occupation": "farmer",
        "income": 1.5,
        "age": 35,
        "gender": "male",
        "state": "Punjab",
        "land_ownership": "yes"
    }
    
    print(f"\nTest user data: {json.dumps(test_user_data, indent=2)}")
    print("\nCalling Bedrock AI to match schemes...")
    
    try:
        matched_schemes = engine.match_schemes(test_user_data)
        print("\n✓ Matching successful!")
        print(f"Matched schemes: {json.dumps(matched_schemes, indent=2)}")
        
        # Check if it's using AI or fallback
        if matched_schemes and "reason" in matched_schemes[0]:
            if len(matched_schemes[0]["reason"]) > 30:
                print("\n✓ BEDROCK AI IS WORKING! (Detailed reasoning)")
                return True
            else:
                print("\n⚠ Using fallback matching (basic reasoning)")
                return False
        else:
            print("\n⚠ No schemes matched")
            return False
            
    except Exception as e:
        print(f"\n✗ Matching failed: {str(e)}")
        return False

def test_response_generation():
    """Test AI-powered response generation"""
    print("\n" + "=" * 60)
    print("TESTING RESPONSE GENERATION (AI)")
    print("=" * 60)
    
    engine = SchemeEngine()
    test_user_data = {"occupation": "farmer", "age": 35}
    test_schemes = [
        {
            "name": "PM Kisan",
            "score": 85,
            "reason": "Farmer with land ownership"
        }
    ]
    
    print(f"\nTest data: {json.dumps(test_user_data, indent=2)}")
    print(f"Test schemes: {json.dumps(test_schemes, indent=2)}")
    print("\nCalling Bedrock AI to generate response...")
    
    try:
        response = engine.generate_response(test_user_data, test_schemes, "en")
        print("\n✓ Response generation successful!")
        print(f"Generated response: {response}")
        
        # Check if it's using AI or fallback
        if len(response) > 50 and "Good news" not in response:
            print("\n✓ BEDROCK AI IS WORKING! (Natural response)")
            return True
        else:
            print("\n⚠ Using fallback response (template)")
            return False
            
    except Exception as e:
        print(f"\n✗ Response generation failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n🚀 AWAAZ BEDROCK AI TEST SUITE\n")
    
    results = {
        "connection": test_bedrock_connection(),
        "extraction": test_user_info_extraction(),
        "matching": test_scheme_matching(),
        "response": test_response_generation()
    }
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.upper()}: {status}")
    
    ai_working = sum(results.values()) >= 3
    
    print("\n" + "=" * 60)
    if ai_working:
        print("🎉 BEDROCK AI IS WORKING!")
        print("Your app is using Claude AI for intelligent scheme matching.")
    else:
        print("⚠️  BEDROCK AI NOT WORKING")
        print("Your app is using fallback rule-based matching.")
        print("\nPossible issues:")
        print("1. AWS credentials not configured correctly")
        print("2. Bedrock model access not enabled")
        print("3. Network/permission issues")
        print("\nCheck your .env file and AWS console.")
    print("=" * 60)

if __name__ == "__main__":
    main()
