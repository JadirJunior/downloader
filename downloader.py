import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import yt_dlp
import os
import re

def hook(d):
    if d['status'] == 'finished':
        progress_bar['value'] = 100
        window.update_idletasks()
        messagebox.showinfo("Download Status", f"Download finished: {d['filename']}")
        reset_fields()
    elif d['status'] == 'downloading':
        # Remove caracteres de escape ANSI
        percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str']).strip('%')
        percent = float(percent_str)
        progress_bar['value'] = percent
        window.update_idletasks()

def download_videos_from_playlist(playlist_url, output_dir='.'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'quiet': False,
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'progress_hooks': [hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def download_button_clicked():
    playlist_url = url_entry.get()
    output_dir = 'downloads'
    download_videos_from_playlist(playlist_url, output_dir)

def reset_fields():
    url_entry.delete(0, tk.END)
    progress_bar['value'] = 0
    window.update_idletasks()

# Create the Tkinter window
window = tk.Tk()
window.title("YouTube Playlist Downloader")
window.geometry("400x200")

# Create a label for the URL input
url_label = tk.Label(window, text="URL:")
url_label.pack()

# Create an entry field for the URL input
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Create a button to trigger the download
download_button = tk.Button(window, text="Download", command=download_button_clicked)
download_button.pack(side=tk.BOTTOM)
download_button.config(height=2, width=20)

# Create a progress bar
progress_bar = Progressbar(window, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
