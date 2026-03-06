import requests
import json

def test_chatbot_port_8000():
    url = "http://localhost:8000/api/chat"
    
    payload = {
        "message": "What is superposition?",
        "context": "quantum_education"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat API working on port 8000!")
            print(f"Response: {result['response'][:100]}...")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Chat API not available on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Chat API on port 8000...")
    test_chatbot_port_8000()