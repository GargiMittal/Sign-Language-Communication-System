import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

# Set working directories if needed
SCRIPT_PATHS = {
    "Sign Language via Camera": "prediction1.py",       # or "prediction1.py"
    "YouTube to ASL": "ytasl2.py",                     # or "YTtoASL.py"
    "Audio to ASL": "AudioToASL.py"
}

# Function to launch a script in a new process
def launch_script(script_name):
    path = SCRIPT_PATHS[script_name]
    python_exe = sys.executable  # Get current Python executable
    subprocess.Popen([python_exe, path])

# GUI setup
root = tk.Tk()
root.title("Unified ASL Translator Hub")
root.geometry("500x400")
root.configure(bg="#eaf6ff")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 14), padding=10)
style.configure("TLabel", font=("Segoe UI", 16, "bold"), background="#eaf6ff")
style.configure("TFrame", background="#eaf6ff")

ttk.Label(root, text="🧏 Signease: ASL Translator Hub").pack(pady=30)

btn_camera = ttk.Button(root, text="Sign Language to Audio translator", command=lambda: launch_script("Sign Language via Camera"))
btn_youtube = ttk.Button(root, text="ASL interpreter for youtube video", command=lambda: launch_script("YouTube to ASL"))
btn_audio = ttk.Button(root, text="Audio to Sign Language translator", command=lambda: launch_script("Audio to ASL"))

btn_camera.pack(pady=15)
btn_youtube.pack(pady=15)
btn_audio.pack(pady=15)

ttk.Label(root, text="Choose a service to begin").pack(pady=30)

root.mainloop()