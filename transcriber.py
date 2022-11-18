# Given path to wav file, return string of spoken words in that file

import speech_recognition as sr
from os import path


def transcribe(audio_file_name):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_name) as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.record(source)  # read the entire audio file

    try:
        transcript = r.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "No words detected"
    return transcript

