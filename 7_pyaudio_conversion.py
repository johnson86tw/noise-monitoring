import numpy as np
import pyaudio
import datetime
import math

# Constants from the TES-1350A manual
V_fs = 0.65  # Full scale voltage in Vrms
db_fs = 100  # Corresponding dB level at full scale in low range

# Calculate the reference voltage for 94 dB SPL
V_94 = V_fs * 10 ** ((94 - db_fs) / 20)


def voltage_to_db_spl(v_rms, v_ref):
    return 20 * np.log10(v_rms / v_ref) + 94


def callback(indata, frames, time, status):
    indata = np.frombuffer(indata, dtype=np.int16)  # Convert to 16-bit integer
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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

print("Recording...")
for _ in range(0, int(RATE / CHUNK * duration)):
    indata = stream.read(CHUNK)
    callback(indata, CHUNK, None, None)

print("Finished recording.")

stream.stop_stream()
stream.close()
audio.terminate()
