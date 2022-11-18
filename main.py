import pyaudio
import asyncio
from is_silence import is_silence
from save_and_transcribe_audio import save_and_transcribe_audio
from aiogram import Bot, Dispatcher, types

api_token = ''

bot = Bot(token=api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

chunk = 2048  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample

channels = 1
fs = 48000  # Record at 44100 samples per second
seconds = 30

last_chunk_silent = True
chunk_silent = True
chunk_buffer = []
p = pyaudio.PyAudio()  # Create an interface to PortAudio

info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

for i in range(0, num_devices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))

print("\nenter ID of desired input device:")

# idi = int(input("\n"))
# if not 0 <= idi < num_devices:
#     idi = 0

idi = 6

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True,
                input_device_index=idi)

sample_width = p.get_sample_size(sample_format)
# Store data in chunks for 3 seconds

# for i in range(0, int(fs / chunk * seconds)):
while True:
    last_chunk_silent = chunk_silent
    data = stream.read(chunk, exception_on_overflow=False)
    chunk_silent = is_silence(data)
    if chunk_silent:
        if not last_chunk_silent and len(chunk_buffer) > 10:
            chunk_buffer.append(data)

            chunk_out = chunk_buffer[:]
            asyncio.run(save_and_transcribe_audio(chunk_out, sample_width,
                                                  bot, dp, sample_rate=fs, channels=channels))
            chunk_buffer = [data]
        else:
            chunk_buffer = [data]

    else:

        chunk_buffer.append(data)

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# # Terminate the PortAudio interface
# p.terminate()
#
# print('Finished recording')
