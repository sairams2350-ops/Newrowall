import requests
import time
import subprocess
import sys
import threading

import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def create_admin():
    print("Waiting for Backend to stay up...")
    for i in range(30):
        try:
            requests.get(f"{API_URL.replace('/api/v1', '')}/health")
            break
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nCreating Admin User...")
    try:
        resp = requests.post(f"{API_URL}/auth/register", json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "is_admin": True
        })
        if resp.status_code == 201:
            print("Admin created successfully.")
        elif resp.status_code == 400 and "already exists" in resp.text:
            print("Admin already exists.")
        else:
            print(f"Failed to create admin: {resp.text}")
    except Exception as e:
        print(f"Error creating admin: {e}")

def run_real_agent():
    print("Starting Simulated Agent in background...")
    # Run in a separate process
    return subprocess.Popen([sys.executable, "simulate_agent.py"])

def run_attack():
    print("Triggering Attack Simulation...")
    try:
        subprocess.run([sys.executable, "simulate_attack.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Attack simulation failed: {e}")

def main():
    # 1. Create Admin
    create_admin()
    
    # 2. Start Agent
    agent_process = run_real_agent()
    
    # Wait for agent to register and send some data
    print("Waiting 10 seconds for agent to generate baseline traffic...")
    time.sleep(10)
    
    # 3. Simulate Attack
    run_attack()
    
    print("\n" + "="*50)
    print("DEMO READY!")
    print("1. Dashboard: http://localhost:3000")
    print("   - Login: admin / admin123")
    print("   - View 'Rules', 'Telemetry', 'Alerts'")
    print("2. Agent is running in background (PID: {}).".format(agent_process.pid))
    print("3. Attack simulation sent.")
    print("3. Attack simulation sent.")
    print("To stop agent, kill the python process.")
    print("="*50 + "\n")
    
    # Get a token for verification
    admin_token = None
    try:
        r = requests.post(f"{API_URL}/auth/login", data={"username": "admin", "password": "admin123"})
        if r.status_code == 200:
            admin_token = r.json()["access_token"]
    except:
        pass

    try:
        while True:
            time.sleep(5)
            # Verify stats
            if admin_token:
                try:
                    stats = requests.get(f"{API_URL}/telemetry/stats", headers={"Authorization": f"Bearer {admin_token}"}).json()
                    print(f"[VERIFY] Backend DB has {stats.get('total_logs', 0)} logs (Allowed: {stats.get('allowed', 0)}, Denied: {stats.get('denied', 0)})")
                except Exception as e:
                    print(f"[VERIFY] Failed to fetch stats: {e}")
    except KeyboardInterrupt:
        print("Stopping agent...")
        agent_process.terminate()

if __name__ == "__main__":
    main()
