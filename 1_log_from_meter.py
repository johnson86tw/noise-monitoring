import sounddevice as sd
import numpy as np
import datetime


def log_decibels(duration, device_index=2, filename="decibel_log.txt"):
    # Open a file to log the decibel levels
    with open(filename, 'a') as f:
        def callback(indata, frames, time, status):
            # Adjust normalization factor as needed
            volume_norm = np.linalg.norm(indata) * 10
            # Convert to decibels
            db = 20 * np.log10(volume_norm) if volume_norm > 0 else -np.inf
            log_entry = f"{datetime.datetime.now()} - {db:.2f} dB\n"
            print(log_entry, end='')
            f.write(log_entry)

        with sd.InputStream(callback=callback, device=device_index):
            sd.sleep(duration * 1000)


if __name__ == "__main__":
    log_decibels(1)
