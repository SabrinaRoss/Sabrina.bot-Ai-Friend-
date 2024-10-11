import sounddevice as sd

def device_populate():
    devices = sd.query_devices()
    device_list = []
    for i, device in enumerate(devices):
        if device['max_output_channels'] > 0:
            device_list.append((i, device["name"]))
    return device_list

def filter_devices(devices):
    filtered = devices
    return filtered[:12]

def audio_secteted(event, device_selected):
    selected_index = int(device_selected.get().split(':')[0])
    return selected_index
