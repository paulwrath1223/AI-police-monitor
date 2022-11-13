# Returns true if the audio sample is deemed to be silence, temporary solution here
# in effect a squelch algorithm

def is_silence(audio):
    return max(audio) < 10
