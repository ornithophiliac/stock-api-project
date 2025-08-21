import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Stock Price API")
    print("=" * 50)
    
    # Test 1: Home endpoint
    print("\n1. Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Companies endpoint
    print("\n2. Testing companies endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/companies")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Date range endpoint
    print("\n3. Testing date range endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/date_range")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Get stock data (valid request)
    print("\n4. Testing get_stock with valid data...")
    try:
        response = requests.get(f"{BASE_URL}/get_stock?company=AAPL&date=2023-07-10")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Get stock data (invalid company)
    print("\n5. Testing get_stock with invalid company...")
    try:
        response = requests.get(f"{BASE_URL}/get_stock?company=INVALID&date=2023-07-10")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Get stock data (missing parameters)
    print("\n6. Testing get_stock with missing parameters...")
    try:
        response = requests.get(f"{BASE_URL}/get_stock?company=AAPL")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()