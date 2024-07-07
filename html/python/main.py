import os
from dotenv import load_dotenv
from pvrecorder import PvRecorder

load_dotenv()


api_key = os.getenv('API_KEY')

for index, device in enumerate(PvRecorder.get_audio_devices()):
    print(f"[{index}] {device}")


recorder  =  PvRecorder(deviceq_index=-1,frame_length=512)
audio = []
try:
    recorder.start()

    while True:
        fname = recorder.read()
        audio.extend(frame)
        

except KeyboardInterrupt:
    recorder.stop()
finally:
    recorder.delete()
