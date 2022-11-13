# Save audio as wav file, named after current time and date
import wave
from datetime import datetime as dt
import os
from transcriber import transcribe
import json
from notifier import notify
import asyncio

folder_name = "transmission history"


async def save_and_transcribe_audio(audio_in, sample_width, sample_rate=44100, channels=1):

    audio = audio_in.copy  # copy the audio before the next chunk is reached

    time = dt.now()
    stringtime = time.strftime("%m-%d-%Y/%H-%M-%S")
    file_base = folder_name + "/" + stringtime + "_police_message/"

    os.mkdir(file_base)

    audio_file_name = file_base + "audio recording.wav"
    transcript_file_name = file_base + "transcript.txt"

    wf = wave.open(audio_file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(audio))
    wf.close()

    transcript = transcribe(audio_file_name)

    with open(transcript_file_name, 'w') as f:
        f.write(transcript)
    f.close()

    a_file = open("keywords.json", "r")
    output = a_file.read()
    a_file.close()
    dic = dict(json.loads(output))
    keywords = list(dic)

    for keyword in keywords:
        if keyword in transcript:
            notify(file_base, keyword)





