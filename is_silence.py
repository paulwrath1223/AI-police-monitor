# Returns true if the audio sample is deemed to be silence, temporary solution here
# in effect a squelch algorithm

def is_silence(audio):
    for byte in audio:
        if 30 < byte < 225:

            return False
    return True
