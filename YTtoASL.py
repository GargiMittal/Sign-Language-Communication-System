import cv2
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
from youtube_transcript_api import YouTubeTranscriptApi

# Get YouTube captions
def get_youtube_transcript(video_id):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# Convert caption list to plain text
def convert_transcript_to_text(transcript):
    return " ".join(entry['text'] for entry in transcript)

# Play ASL videos in a single persistent window
def convert_text_to_asl_videos(text):
    window_name = "ASL Translator"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    for letter in text:
        if letter.isalpha():
            video_path = f"gifs/{letter.upper()}.mp4"
            if not os.path.exists(video_path):
                print(f"Missing video for {letter}")
                continue

            cap = cv2.VideoCapture(video_path)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow(window_name, frame)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

            cap.release()
            time.sleep(0.2)

    cv2.destroyAllWindows()

# Start ASL process from GUI
def start_translation():
    video_id = entry.get().strip()
    if not video_id:
        messagebox.showwarning("Input Required", "Please enter a YouTube Video ID.")
        return

    transcript = get_youtube_transcript(video_id)
    if transcript:
        text = convert_transcript_to_text(transcript)
        print("Extracted Text:", text)
        convert_text_to_asl_videos(text)
    else:
        messagebox.showerror("Error", "No transcript available or invalid video ID.")

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("YouTube to ASL Translator")
root.geometry("450x300")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12), padding=10)
style.configure("TEntry", font=("Segoe UI", 12))

title = ttk.Label(root, text="🧏 YouTube to ASL Translator", font=("Segoe UI", 16, "bold"))
title.pack(pady=20)

entry_label = ttk.Label(root, text="Enter YouTube Video ID:")
entry_label.pack()

entry = ttk.Entry(root, width=30)
entry.pack(pady=10)

start_button = ttk.Button(root, text="Translate to ASL", command=start_translation)
start_button.pack(pady=20)

note = ttk.Label(root, text="Videos should be placed in asl_videos/ as A.mp4, B.mp4, ...", wraplength=400, justify="center", font=("Segoe UI", 9))
note.pack(pady=10)

root.mainloop()


# wtl5UrrgU8c
# lHfjvYzr-3g
# ukzFI9rgwfU
# O5nskjZ_GoI
# TNQsmPf24go