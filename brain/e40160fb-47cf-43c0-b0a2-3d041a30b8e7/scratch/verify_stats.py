import requests
import json

# Try both global stats and a specific user stats if possible
try:
    # Need to login to get a token because these endpoints are protected
    login_data = {"username": "admin", "password": "password123"} # Assuming default creds from previous context
    r_login = requests.post("http://localhost:8001/auth/login", json=login_data)
    if r_login.status_code == 200:
        token = r_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        r = requests.get("http://localhost:8001/api/dashboard/stats", headers=headers)
        print(f"Stats Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()["data"]
            print("Dashboard Stats Data:")
            print(json.dumps(data, indent=2))
            if "avgCredit" in data:
                print(f"SUCCESS: avgCredit found: {data['avgCredit']}")
            else:
                print("FAILURE: avgCredit MISSING from response")
    else:
        print(f"Login failed: {r_login.status_code}")
except Exception as e:
    print(f"Error: {e}")
