import requests
import json

# Test the chat API
def test_chatbot():
    url = "http://localhost:8002/api/chat"
    
    test_messages = [
        "What is superposition?",
        "Explain quantum entanglement",
        "How does a Hadamard gate work?",
        "What is the Bloch sphere?"
    ]
    
    for message in test_messages:
        print(f"\n🧪 Testing: {message}")
        
        payload = {
            "message": message,
            "context": "quantum_education"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"🤖 Response: {result['response'][:100]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Backend not running on port 8002")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Chatbot API...")
    test_chatbot()
    print("\n✅ Test completed!")