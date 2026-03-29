import requests
import json
import random
import time
from datetime import datetime, timezone

import os

# Config
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def login():
    try:
        response = requests.post(f"{API_URL}/auth/login", data={"username": "admin", "password": "admin123"})
        if response.status_code == 200:
            return response.json()["access_token"]
    except Exception as e:
        print(f"Login failed: {e}")
    return None

def trigger_attack():
    token = login()
    if not token:
        print("Could not log in.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get Device (we need a valid device ID)
    devices = requests.get(f"{API_URL}/devices/", headers=headers).json()
    if not devices:
        print("No devices found. Run real_agent.py first!")
        return
    
    target_device = devices[0]
    device_id = target_device["id"]
    print(f"Targeting Device: {target_device['hostname']} (ID: {device_id})")

    # 2. Construct Malicious Payload (Data Exfiltration Simulation)
    # A massive spike in bytes_sent usually indicates data theft or C2 communication
    attack_log = {
        "device_id": device_id,
        "process_id": 1337,
        "process_name": "powershell.exe",
        "protocol": "tcp",
        "direction": "outbound",
        "source_ip": "192.168.1.100",
        "source_port": 54321,
        "destination_ip": "185.100.100.100", # Suspicious IP
        "destination_port": 443,
        "domain": "malicious-c2.com",
        "bytes_sent": 50000000, # 50 MB (Huge spike compared to normal KB)
        "bytes_received": 100,
        "action_taken": "allow", # Firewall let it through, AI must catch it!
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "application_id": None
    }

    print("\n[ ATTACK SIMULATION STARTED ]")
    print(f"Sending massive 50MB payload telemetry from {attack_log['process_name']}...")
    
    response = requests.post(f"{API_URL}/telemetry/", json=attack_log, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print("\n[ SUCCESS ] Telemetry sent.")
        print(f"Server Analysis Result:")
        print(f" - Is Anomaly: {data.get('is_anomaly')}")
        print(f" - Z-Score: {data.get('z_score')}")
        
        if data.get('is_anomaly'):
            print("\n>>> AI DETECTED THE ATTACK! <<<")
            print("Check your Dashboard 'Alerts' section immediately.")
        else:
            print("\nAI did not flag it. The baseline might not be established yet.")
            print("Run real_agent.py for longer to build a traffic baseline.")
    else:
        print(f"Failed: {response.text}")

if __name__ == "__main__":
    trigger_attack()
