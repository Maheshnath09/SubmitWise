import requests
import json
import time

API_URL = "http://localhost:8000"

def verify_api():
    # 1. Register
    print("Registering...")
    email = f"test_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "password": "password123",
        "role": "student"
    }
    try:
        response = requests.post(f"{API_URL}/api/auth/register", json=payload)
        response.raise_for_status()
        data = response.json()
        token = data["access_token"]
        print(f"Registered successfully. Token: {token[:10]}...")
    except Exception as e:
        print(f"Registration failed: {e}")
        if response:
            print(response.text)
        return

    # 2. Generate Project
    print("Generating Project...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    project_payload = {
        "subject": "Python Automation",
        "semester": 5,
        "difficulty": "Beginner",
        "additional_requirements": "Use requests library"
    }
    
    try:
        response = requests.post(f"{API_URL}/api/projects/generate", json=project_payload, headers=headers)
        response.raise_for_status()
        project_data = response.json()
        print(f"Generation started. Job ID: {project_data['job_id']}")
        
        # Poll status
        job_id = project_data['job_id']
        for _ in range(10):
            time.sleep(2)
            status_res = requests.get(f"{API_URL}/api/projects/{job_id}/status", headers=headers)
            status_data = status_res.json()
            print(f"Status: {status_data['status']}")
            if status_data['status'] == 'completed':
                print("Generation completed successfully!")
                break
            if status_data['status'] == 'failed':
                print("Generation failed!")
                break
                
    except Exception as e:
        print(f"Generation failed: {e}")
        if response:
            print(response.text)

if __name__ == "__main__":
    verify_api()
