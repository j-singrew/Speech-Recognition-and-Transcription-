import requests
from conigure import API_KE_ASSEMBLYAI
import sys
import time

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

filename = sys.argv[1]

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

try:
    with open(filename, 'rb') as file:
        pass
except FileNotFoundError:
    print("Error: File not found. Please provide a valid file path.")
    sys.exit(1)

header = {
    'authorization': API_KE_ASSEMBLYAI,
    'content-type': 'application/json'
}

response = requests.post(upload_endpoint, headers=header, data=read_file(filename))
upload_url = response.json()["upload_url"]

def initiate_transcription(upload_url):
    data = {
        "audio_url": upload_url
    }
    response = requests.post(transcription_endpoint, headers=header, json=data)
    return response.json()

def poll_transcription_status(transcription_id):
    while True:
        response = requests.get(f"{transcription_endpoint}/{transcription_id}", headers=header)
        status = response.json()["status"]
        if status == "completed":
            return response.json()["text"]
        elif status == "failed":
            return None
        else:
            time.sleep(5)

transcription_response = initiate_transcription(upload_url)
transcription_id = transcription_response["id"]
transcript = poll_transcription_status(transcription_id)

if transcript:
    print("Transcription completed:")
    print(transcript)
    with open("transcription.txt", "w") as file:
        file.write(transcript)
else:
    print('Transcription failed.')
