import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
BASE_URL = "https://api.assemblyai.com/v2"
HEADERS = {"authorization": API_KEY}
FILE = os.getenv("file")



file_path = f"/Users/joshuasingrew/Downloads/{FILE}"


with open(file_path, 'rb') as f:
    upload_response = requests.post(f"{BASE_URL}/upload", headers=HEADERS, data=f)

if upload_response.status_code != 200:
    print(f"❌ Upload failed: {upload_response.status_code}, {upload_response.text}")
    upload_response.raise_for_status()

upload_url = upload_response.json()["upload_url"]
print(f"✅ File uploaded successfully! URL: {upload_url}")


transcript_request = {"audio_url": upload_url}
transcript_response = requests.post(f"{BASE_URL}/transcript", json=transcript_request, headers=HEADERS)

if transcript_response.status_code != 200:
    print(f"❌ Transcription request failed: {transcript_response.status_code}, {transcript_response.text}")
    transcript_response.raise_for_status()

transcript_id = transcript_response.json()["id"]
polling_endpoint = f"{BASE_URL}/transcript/{transcript_id}"


timeout_seconds = 300   
poll_interval = 3       
start_time = time.time()

print("\n⏳ Polling for transcription result...\n")

while True:
    elapsed = time.time() - start_time
    if elapsed > timeout_seconds:
        print(f"⏰ Timeout reached after {timeout_seconds // 60} minutes.")
        raise TimeoutError("Transcription polling timed out.")

    transcript = requests.get(polling_endpoint, headers=HEADERS).json()
    status = transcript["status"]

    if status == "completed":
        print("\n✅ Transcription completed successfully!\n")
        print("Full Transcript:\n")
        print(FILE)
        
        print(transcript["text"])
        break

    elif status == "error":
        raise RuntimeError(f"❌ Transcription failed: {transcript['error']}")

    else:
        print(f"Status: {status} — elapsed: {int(elapsed)}s, retrying in {poll_interval}s...")
        time.sleep(poll_interval)
