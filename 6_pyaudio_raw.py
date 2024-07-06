import pyaudio
import numpy as np
import datetime


def log_decibels(duration, device_index=2, filename='raw_output_signals.txt'):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)

    with open(filename, 'w') as f:
        print("Recording...")
        for _ in range(0, int(RATE / CHUNK * duration)):
            indata = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            log_entry = f"{datetime.datetime.now()} - {indata}\n"
            print(log_entry, end='')
            f.write(log_entry)

        print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == "__main__":
    log_decibels(1)
