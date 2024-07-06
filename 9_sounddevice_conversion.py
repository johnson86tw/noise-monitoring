import numpy as np
import sounddevice as sd
import datetime

# ==============================================================================
#
# 這是用 8_ 請 chatgpt 將 pyaudio 轉換成 sounddevice 的程式碼
#
# ==============================================================================

# Constants from the TES-1350A manual
V_fs = 0.65  # Full scale voltage in Vrms
db_fs = 100  # Corresponding dB level at full scale in low range

# Calculate the reference voltage for 94 dB SPL
V_94 = V_fs * 10 ** ((94 - db_fs) / 20)


def voltage_to_db_spl(v_rms, v_ref):
    return 20 * np.log10(v_rms / v_ref) + 94


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    indata = np.squeeze(indata)  # Convert to 1D array
    max_int_value = 2**15  # 32768 for 16-bit PCM

    # Scale the integer data to voltage
    voltage_data = indata / max_int_value * V_fs

    squared_data = np.square(voltage_data)
    mean_squared_data = np.mean(squared_data)
    rms_voltage = np.sqrt(mean_squared_data)

    # Calculate the RMS voltage of the input signal
    print(f"RMS Voltage: {rms_voltage:.6f} V", flush=True)

    # Convert the RMS voltage to decibels (A-weighted)
    db_spl = voltage_to_db_spl(rms_voltage, V_94)
    log_entry = f"{datetime.datetime.now()} - {db_spl:.2f} dB(A)\n"
    print(log_entry, end='')


device_index = 2  # Replace with the actual device index
duration = 1  # Replace with the actual duration in seconds

# Parameters for sounddevice
channels = 1
samplerate = 44100
blocksize = 1024

print("Recording...")
with sd.InputStream(callback=callback, device=device_index, channels=channels,
                    samplerate=samplerate, blocksize=blocksize):
    sd.sleep(int(duration * 1000))

print("Finished recording.")
