import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import threading
import scipy.io.wavfile as wav
import src.universal_src.audio_output as audio_output
from text_to_speech import TTS 
import time
from speach_to_text import SpeechRecognition
import claude_chat as cc
from src.universal_src.file_manager import FileManager
program_device_index = None
headphones_device_index = None

#filepath locating stuffed but should work... hopefully
audio_file_path = FileManager.level_one_directory_search("VTS_Audio_Cache", "audio_cache.wav")

tts = TTS()
file_lock = threading.Lock()
recogniser = SpeechRecognition()
debounce_time = .3
last_space_time = 0
is_button_held = False
listen_thread = None

prompt = ""
results = [""]

def listen(stop_event):
    global results
    global prompt
    while not stop_event.is_set():
        if not recogniser.is_listening:
            recogniser.start_listening()
        time.sleep(.1)
    if recogniser.is_listening:
        results = recogniser.stop_listening()
        print(results)
        prompt = cc.submit_prompt(results[0])


def on_program_device_selected(event):
    global program_device_index
    selected_index = int(device_dropdown_vb_cable.get().split(':')[0])
    program_device_index = selected_index
    if headphones_device_index is not None:
        play_audio_on_devices(program_device_index, headphones_device_index)

def on_headphones_device_selected(event):
    global headphones_device_index
    selected_index = int(headphones_device_var.get().split(':')[0])
    headphones_device_index = selected_index
    if program_device_index is not None:
        play_audio_on_devices(program_device_index, headphones_device_index)


def retrieve_wav(text=""):
    tts.get_audio_onto_file(text, audio_file_path)

def play_audio(device_index):
    samplerate, audio_data = wav.read(audio_file_path)
    sd.play(audio_data, samplerate=samplerate, device=device_index)
    sd.wait()

def play_button_clicked():
    play_button.config(state=tk.DISABLED)
    if program_device_index is not None and headphones_device_index is not None:
        retieve_thread = threading.Thread(target=retrieve_wav, args=(prompt,))
        retieve_thread.start()
        retieve_thread.join()
        thread1 = threading.Thread(target=play_audio, args=(program_device_index,))
        thread2 = threading.Thread(target=play_audio, args=(headphones_device_index,))

        thread1.start()
        thread2.start()

        def reenable_button():
            thread1.join()
            thread2.join()
            play_button.config(state=tk.NORMAL)
        threading.Thread(target=reenable_button).start()

def on_button_press(event):
    global is_button_held
    global last_space_time
    global listen_thread
    global stop_event

    is_button_held = True
    last_space_time = time.time()

    # Create a new event for stopping the thread
    stop_event = threading.Event()

    if listen_thread is None or not listen_thread.is_alive():
        listen_thread = threading.Thread(target=listen, args=(stop_event,))
        listen_thread.start()
    canvas.itemconfig(circle_button, fill="red")

def on_button_release(event):
    global is_button_held
    global stop_event

    is_button_held = False
    if listen_thread is not None:
        stop_event.set()  # Signal the listening thread to stop
        listen_thread.join()  # Wait for the thread to finish
        results = recogniser.stop_listening()
        if results:
             print("User said:", " ".join(results))
    canvas.itemconfig(circle_button, fill="blue")
    root.update_idletasks() 
    
def create_circle_button(canvas, x, y, r, **kwargs):
    circle = canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    return circle

#setup the window
root = tk.Tk()
root.title("VTS Support App")
root.geometry("400x300")

device_list = audio_output.device_populate()
filtered_device_list = audio_output.filter_devices(device_list)

#select audio device for vb cable
device_dropdown_vb_cable = tk.StringVar()
device_dropdown_vb_cable = ttk.Combobox(root, textvariable=device_dropdown_vb_cable, state="readonly")
device_dropdown_vb_cable['values'] = [f"{index}: {name}" for index, name in filtered_device_list]
device_dropdown_vb_cable.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
device_dropdown_vb_cable.bind("<<ComboboxSelected>>", on_program_device_selected)

#select audio device for main audio device
headphones_device_var = tk.StringVar()
headphones_device_dropdown = ttk.Combobox(root, textvariable=headphones_device_var, state="readonly")
headphones_device_dropdown['values'] = [f"{index}: {name}" for index, name in filtered_device_list]
headphones_device_dropdown.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
headphones_device_dropdown.bind("<<ComboboxSelected>>", on_headphones_device_selected)
# Play button
play_button = tk.Button(root, text="Play Audio", command=play_button_clicked)
play_button.grid(row=2, column=0, padx=10, pady=10)

canvas = tk.Canvas(root, width=100, height=100, bg="white")
canvas.grid(row=3, column=0, padx=10, pady=10)
circle_button = create_circle_button(canvas, 50, 50, 40, fill="blue")
canvas.tag_bind(circle_button, "<ButtonPress-1>", on_button_press)
canvas.tag_bind(circle_button, "<ButtonRelease-1>", on_button_release)

root.mainloop()