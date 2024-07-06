import pyaudio


def find_usb_device_index():
    p = pyaudio.PyAudio()
    usb_device_index = None

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device Index: {i}, Device Name: {device_info['name']}")

        # Check if the device name contains 'USB'
        if 'USB' in device_info['name']:
            usb_device_index = i
            print(f"Found USB device at index: {usb_device_index}")

    p.terminate()

    if usb_device_index is None:
        print("No USB device found")
    return usb_device_index


# Find and print the USB device index
usb_index = find_usb_device_index()
print(f"USB Device Index: {usb_index}")
