import sounddevice as sd
import numpy as np
import datetime


# Function to convert RMS voltage to decibels
def voltage_to_db(voltage):
    return 20 * np.log10(voltage) if voltage > 0 else -np.inf


def log_decibels(duration, device_index=2):

    def callback(indata, frames, time, status):
        # Flatten the array to a single dimension
        flat_indata = indata.flatten()
        # Calculate the RMS voltage of the input signal
        rms_voltage = np.sqrt(np.mean(flat_indata**2))
        # Convert the RMS voltage to decibels
        db = voltage_to_db(rms_voltage)
        log_entry = f"{datetime.datetime.now()} - {db:.2f} dB\n"
        print(log_entry, end='')

    with sd.InputStream(callback=callback, device=device_index):
        sd.sleep(duration * 1000)


if __name__ == "__main__":
    # Run for 1 seconds
    log_decibels(1)
