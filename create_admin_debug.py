import requests

API_URL = "http://localhost:8000/api/v1"

def create_admin():
    print("Creating Admin User...")
    try:
        resp = requests.post(f"{API_URL}/auth/register", json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "is_admin": True
        })
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        
    except Exception as e:
        print(f"Error creating admin: {e}")

if __name__ == "__main__":
    create_admin()
