import os
import signal
import soundfile as sf
from dotenv import load_dotenv
from pvrecorder import PvRecorder
import numpy as np
import pyaudio

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv('API_KEY')

# List available audio devices using pyaudio
p = pyaudio.PyAudio()
print("Available audio devices:")
for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")
p.terminate()

# Set device index and parameters
device_index = 0  # Change to your preferred device index
frame_length = 512
sample_rate = 16000  # Change this to your desired sample rate

# Initialize the recorder
recorder = None
try:
    recorder = PvRecorder(device_index=device_index, frame_length=frame_length)
except Exception as e:
    print(f"Failed to initialize recorder: {e}")
    exit(1)

audio = []

def signal_handler(sig, frame):
    global recorder
    try:
        if recorder:
            recorder.stop()
            recorder.delete()
        # Save the recorded audio to a file
        audio_data = np.array(audio, dtype=np.int16)
        sf.write('recorded_audio.wav', audio_data, sample_rate)
        print("Recording stopped and saved to 'recorded_audio.wav'.")
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
        except Exception as e:
            print(f"Error in finally block while stopping recorder: {e}")
        try:
            recorder.delete()
        except Exception as e:
            print(f"Error deleting recorder in finally block: {e}")
