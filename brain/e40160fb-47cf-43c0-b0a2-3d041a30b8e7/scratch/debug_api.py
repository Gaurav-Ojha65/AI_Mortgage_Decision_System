import requests
import json

try:
    r = requests.get("http://localhost:8001/api/models/comparison")
    print(f"Status: {r.status_code}")
    try:
        data = r.json()
        print("Success: Valid JSON received")
        print(json.dumps(data, indent=2)[:500] + "...")
    except Exception as e:
        print(f"Error: Invalid JSON received: {e}")
        print(f"Response text: {r.text[:500]}")
except Exception as e:
    print(f"Error: Connection failed: {e}")
