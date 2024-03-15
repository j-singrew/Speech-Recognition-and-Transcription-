import requests # import the requests library,which is used for making  HTTP requests.
from configure import API_KE_ASSEMBLYAI #  import the AssemblyAI  API key from the configure.py file.
import sys # import the sys module ,which provides access to some  variables  used or maintained by the python  interpreter and that interacts strongly with the interpreter.
import time # imports the time module for adding delays.

# Defining  the endpoint for uploading  and the recieving of transcriptions from AssemblyAI.
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

# getting the filename of the audio file to be transcibed from command-line argunemnts.
filename = sys.argv[1]

# function to read the audio  fiel in chunks.
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

# Error handeling: checking if  the   file exists.
try:
    with open(filename, 'rb') as file:
        pass
except FileNotFoundError:
    print("Error: File not found. Please provide a valid file path.")
    sys.exit(1) # exiting  the script with a status  code of 1 wich indicates a error

#Setting up the requests headers with the AssemblyAI API Key.
header = {
    'authorization': API_KE_ASSEMBLYAI,
    'content-type': 'application/json'
}

# upload audio file  to AssemblyAI  and obtain the uplaod URL
response = requests.post(upload_endpoint, headers=header, data=read_file(filename))
upload_url = response.json()["upload_url"]

#Function to iniate transcription
def initiate_transcription(upload_url):
    data = {
        "audio_url": upload_url
    }
    response = requests.post(transcription_endpoint, headers=header, json=data)
    return response.json()

# function to poll AssmeblyAI API for the status of the transcription.
def poll_transcription_status(transcription_id):
    while True:
        response = requests.get(f"{transcription_endpoint}/{transcription_id}", headers=header)
        status = response.json()["status"]
        if status == "completed":
            return response.json()["text"]
        elif status == "failed":
            return None
        else:
            time.sleep(5) # waiting 5 seconds before polling again.

# initiating the transcription status and retrieving the transcription ID.
transcription_response = initiate_transcription(upload_url)
transcription_id = transcription_response["id"]

#polling for transcription status and recieving transcription if availabale.
transcript = poll_transcription_status(transcription_id)

if transcript:
    print("Transcription completed:")
    print(transcript)
    with open("transcription.txt", "w") as file:
        file.write(transcript)
else:
    print('Transcription failed.')
