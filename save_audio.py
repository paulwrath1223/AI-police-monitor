# Save audio as wav file, named after current time and date
import wave
from datetime import datetime as dt

folder_name = "transcript history"


def save_audio(audio, sample_width, sample_rate=44100, channels=1):
    time = dt.now()
    stringtime = time.strftime("%m-%d-%Y_%H-%M-%S")
    filename = folder_name + "/" + stringtime + "_police_message.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(audio))
    wf.close()





