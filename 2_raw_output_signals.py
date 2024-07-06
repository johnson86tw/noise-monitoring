import sounddevice as sd
import numpy as np
import datetime


def log_decibels(duration, device_index=2, filename='raw_output_signals.txt'):

    with open(filename, 'w') as f:
        def callback(indata, frames, time, status):
            log_entry = f"{datetime.datetime.now()} - {indata}\n"
            print(log_entry, end='')
            f.write(log_entry)

        with sd.InputStream(callback=callback, device=device_index):
            sd.sleep(duration * 1000)


if __name__ == "__main__":
    log_decibels(1)
