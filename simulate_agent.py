import json
import time
import random
import urllib.request
import urllib.error
import urllib.parse
import sys
from datetime import datetime

import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
USERNAME = "admin"
PASSWORD = "admin123"
DEVICE_ID = "simulation-pc-001"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def make_request(endpoint, method="GET", data=None, token=None):
    url = f"{API_URL}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Handle Form data for login specifically if needed, but our login is Form...
    # Wait, I changed login to use Form data in the previous step.
    # So for login, we need `application/x-www-form-urlencoded`.
    
    if endpoint == "auth/login":
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        # data should be a dict here, we convert to urlencoded bytes
        payload = urllib.parse.urlencode(data).encode('utf-8')
    else:
        if data:
            payload = json.dumps(data).encode('utf-8')
        else:
            payload = None

    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status >= 200 and response.status < 300:
                return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        log(f"Request failed: {e.code} - {error_body}")
        sys.exit(1)
    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)

def main():
    log("🚀 Starting NeuroWall Simulation Agent")
    
    # 1. Login
    log("🔑 Logging in as admin...")
    login_data = {"username": USERNAME, "password": PASSWORD}
    auth_response = make_request("auth/login", "POST", login_data)
    token = auth_response["access_token"]
    log("✅ Login successful")

    # 2. Register Device
    log(f"💻 Registering device: {DEVICE_ID}...")
    device_data = {
        "device_id": DEVICE_ID,
        "hostname": "Simulation-PC",
        "platform": "Windows 11",
        "ip_address": "192.168.1.105",
        "mac_address": "00:11:22:33:44:55",
        "agent_version": "1.0.0-sim"
    }
    device_response = make_request("devices/", "POST", device_data, token)
    log("✅ Device registered")

    # Get the numeric ID from the response (assuming response is the device object)
    # The API returns DeviceResponse which has 'id'
    db_device_id = None
    if isinstance(device_response, dict) and 'id' in device_response:
        db_device_id = device_response['id']
    else:
        log("❌ Failed to get device ID from registration response")
        sys.exit(1)

    log(f"✅ Device registered with DB ID: {db_device_id}")

    # 3. Telemetry Loop
    log("📡 Starting telemetry stream (Ctrl+C to stop)...")
    
    apps = [
        ("chrome.exe", "tcp", 443, "google.com"),
        ("spotify.exe", "tcp", 4070, "spotify.com"),
        ("malware.exe", "udp", 666, "evil-site.com"),
        ("teams.exe", "udp", 3478, "microsoft.com"),
        ("powershell.exe", "tcp", 80, "unknown-ip"),
    ]

    try:
        while True:
            app, protocol, port, domain = random.choice(apps)
            
            # Simple logic: block malware
            action = "deny" if "malware" in app else "allow"
            is_anomaly = "malware" in app
            
            # Use IP for some, domain for others
            dest_ip = f"10.0.{random.randint(1,255)}.{random.randint(1,255)}" if domain == "unknown-ip" else None
            
            telemetry_data = {
                "device_id": db_device_id, 
                "process_id": random.randint(1000, 9999),
                "process_name": app,
                "protocol": protocol,
                "bytes_sent": random.randint(100, 10000),
                "bytes_received": random.randint(100, 10000),
                "action_taken": action,
                "domain": domain if domain != "unknown-ip" else None,
                "destination_ip": dest_ip,
                "destination_port": port,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            make_request("telemetry/", "POST", telemetry_data, token)
            log(f"Sent log: {app} -> {action.upper()}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        log("🛑 Simulation stopped")

if __name__ == "__main__":
    main()
