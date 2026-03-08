"""
Quick API Test Script
Run this to verify all endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n🔍 Testing Root Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_chat():
    """Test chat endpoint"""
    print("\n🔍 Testing Chat API...")
    data = {
        "message": "I am a farmer with 2 acres of land",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_schemes():
    """Test get schemes endpoint"""
    print("\n🔍 Testing Get Schemes...")
    response = requests.get(f"{BASE_URL}/api/schemes")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_generate_affidavit():
    """Test affidavit generation"""
    print("\n🔍 Testing Affidavit Generation...")
    data = {
        "user_name": "Ram Kumar",
        "father_name": "Shyam Kumar",
        "address": "Village Rampur, District Sitapur, UP",
        "purpose": "Income Certificate",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/api/generate-affidavit", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 AWAAZ API TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Chat API", test_chat),
        ("Get Schemes", test_schemes),
        ("Generate Affidavit", test_generate_affidavit)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "✅ PASSED" if passed else "❌ FAILED"))
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append((name, f"❌ ERROR: {str(e)}"))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    for name, result in results:
        print(f"{name}: {result}")
    
    passed_count = sum(1 for _, result in results if "✅" in result)
    total_count = len(results)
    print(f"\n✅ Passed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Your API is ready for demo!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running:")
    print("   cd backend && uvicorn main:app --reload\n")
    
    input("Press Enter to start tests...")
    run_all_tests()
