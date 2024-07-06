import numpy as np
import sounddevice as sd
import datetime
import math

# Constants from the TES-1350A manual
V_fs = 0.65  # Full scale voltage in Vrms
db_fs = 100  # Corresponding dB level at full scale in Hi range


def voltage_to_db(v_rms, v_fs, db_fs):
    return (v_rms / v_fs) * db_fs


def callback(indata, frames, time, status):
    squared_data = np.square(indata)
    mean_squared_data = np.mean(squared_data)
    rms_voltage = np.sqrt(mean_squared_data)

    # Calculate the RMS voltage of the input signal
    print(f"RMS Voltage: {rms_voltage:.6f} V", flush=True)

    log_rms_voltage = math.log10(rms_voltage)

    # Convert the RMS voltage to decibels
    db = voltage_to_db(log_rms_voltage, V_fs, db_fs)
    log_entry = f"{datetime.datetime.now()} - {db:.2f} dB\n"
    print(log_entry, end='')


device_index = 2  # Replace with the actual device index
duration = 1  # Replace with the actual duration in seconds

with sd.InputStream(callback=callback, device=device_index):
    sd.sleep(duration * 1000)
