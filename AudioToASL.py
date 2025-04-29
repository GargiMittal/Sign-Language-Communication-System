import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
import os
from PIL import Image, ImageTk
import cv2
import time
from threading import Thread

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to record audio and convert it to text
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return None

# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to play a video using OpenCV
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame).resize((400, 300))  # Resize for UI
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.config(image=imgtk)
        video_label.image = imgtk
        time.sleep(0.03)
        root.update_idletasks()
    cap.release()

# Function to display ASL videos
def display_asl_video(text):
    video_folder = "gifs"
    for letter in text.upper():
        if letter.isalpha():
            video_path = os.path.join(video_folder, f"{letter}.mp4")
            if os.path.exists(video_path):
                play_video(video_path)
                time.sleep(0.4)  # Shorter delay for smoother experience

# Full process: speech recognition → TTS → ASL video
def start_process():
    def task():
        text = record_audio()
        if text:
            speak_text(text)
            display_asl_video(text)
        else:
            messagebox.showerror("Error", "Could not recognize speech.")
    Thread(target=task, daemon=True).start()

# Set up the GUI
root = tk.Tk()
root.title("ASL Translator")
root.geometry("500x400")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 14), padding=10)
style.configure("TLabel", font=("Segoe UI", 12), background="#f4f4f4")

# Title Label
title_label = ttk.Label(root, text="ASL Audio to Video Translator", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=10)

# Start Button
start_button = ttk.Button(root, text="Start Recording", command=start_process)
start_button.pack(pady=20)

# Video display label
video_label = tk.Label(root, bg="#f4f4f4")
video_label.pack(pady=10, expand=True)

# Run app
root.mainloop()
