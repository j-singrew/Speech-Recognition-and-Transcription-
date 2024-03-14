import requests
from conigure import API_KE_ASSEMBLYAI
import sys

upload_endpoint = "https://api.assemblyai.com/v2/upload"
#endpoint =

filename =  sys.argv[1]

#uplaod audio

#read Audio file
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

header = {'authorization':API_KE_ASSEMBLYAI,
          'content-type' :'application/json'
 }
response = requests.post(upload_endpoint,
                         headers=header,
                         data=read_file(filename))
print(response.json())

#transcribe


#poll assembly AI API


# save transcript
