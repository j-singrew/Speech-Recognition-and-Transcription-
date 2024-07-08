import os
import signal
import soundfile as sf
from dotenv import load_dotenv
from pvrecorder import PvRecorder
import numpy as np
import pyaudio
import requests

# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv('API_KEY')

audio_file_path = "recorded_audio.wav"
endpoint = "https://api.assemblyai.com/v2/upload"

# List available audio devices using pyaudio
p = pyaudio.PyAudio()
print("Available audio devices:")
for index, device in enumerate(PvRecorder.get_available_devices()):  # Remove `p` from here
    print(f"[{index}] {device}")
p.terminate()

# Set device index and parameters
device_index = 0  # Change to your preferred device index
frame_length = 512
sample_rate = 16000  # Change this to your desired sample rate

# Initialize the recorder
recorder = None
try:
    recorder = PvRecorder(device_index=device_index, frame_length=frame_length, sample_rate=sample_rate)
except Exception as e:
    print(f"Failed to initialize recorder: {e}")
    exit(1)

audio = []

def signal_handler(sig, frame):
    global recorder
    try:
        if recorder:
            recorder.stop()
            # Save the recorded audio to a file
            audio_data = np.array(audio, dtype=np.int16)
            sf.write(audio_file_path, audio_data, sample_rate)
            print(f"Recording stopped and saved to '{audio_file_path}'.")
    except Exception as e:
        print(f"Error stopping recorder in signal handler: {e}")
    exit(0)

# Register the signal handler for graceful exit
signal.signal(signal.SIGINT, signal_handler)

try:
    recorder.start()
    print("Recording started. Press Ctrl+C to stop.")

    while True:
        frame = recorder.read()
        audio.extend(frame)

except KeyboardInterrupt:
    signal_handler(None, None)
except Exception as e:
    print(f"Error during recording: {e}")
finally:
    if recorder:
        try:
            recorder.stop()
            recorder.delete()
        except Exception as e:
            print(f"Error in finally block while stopping recorder: {e}")

headers = {
    "authorization": api_key,
    "content-type": "audio/wav"
}

try:
    with open(audio_file_path, "rb") as file:
        response = requests.post(endpoint, headers=headers, files={"file": file})
        if response.status_code == 201:
            upload_url = response.json().get('upload_url')
            print(f"Upload successful. File can be accessed at: {upload_url}")
        else:
            print(f"Failed to upload audio file. Status code: {response.status_code}")
except IOError as e:
    print(f"Error reading audio file: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error uploading audio file: {e}")
