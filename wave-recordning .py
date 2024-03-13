import pyaudio
import wave

FRAMES_PER_BUFFER = 3200
Format = pyaudio.paInt16
CHANNELS =1
RATE =16000

P = pyaudio.PyAudio()

stream = P.open(
    format=Format,
    channels = CHANNELS,
    rate =RATE,
    input=True,
    frames_per_buffer = FRAMES_PER_BUFFER
)
print("Start recordin")

seconds = 5
frames = []
for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
P.terminate()

obj = wave.open("output.wave","wb")
obj.setnchannels(CHANNELS)
obj.setframerate(RATE)
obj.setsampwidth(P.get_sample_size(Format))
obj.writeframes(b"".join(frames))
obj.close()


