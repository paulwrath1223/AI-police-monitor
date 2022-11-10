import pyaudio
import wave
from is_silence import is_silence
from save_audio import save_audio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
# sample_format = pyaudio.paFloat32  # TEST
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3

last_chunk_silent = True
chunk_silent = True
chunk_buffer = []
p = pyaudio.PyAudio()  # Create an interface to PortAudio

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

idi = 1

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
#
#
# print("\nenter ID of desired input device:")
#
# idi = int(input("\n"))
# if not 0 <= idi < numdevices:
#     idi = 0

print('Recording')


stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True,
                input_device_index=idi)

frames = []  # Initialize array to store frames
sample_width = p.get_sample_size(sample_format)
# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    last_chunk_silent = chunk_silent
    data = stream.read(chunk)
    chunk_silent = is_silence(data)
    if chunk_silent:
        if last_chunk_silent:
            chunk_buffer = data
        else:
            chunk_buffer.append(data)
            save_audio(chunk_buffer, sample_width, sample_rate=fs, channels=channels)
    else:
        chunk_buffer.append(data)


# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print(p.get_sample_size(sample_format))
print('Finished recording')

# Save the recorded data as a WAV file
# wf = wave.open(filename, 'wb')
# wf.setnchannels(channels)
# wf.setsampwidth(p.get_sample_size(sample_format))
# wf.setframerate(fs)
# wf.writeframes(b''.join(frames))
# wf.close()
