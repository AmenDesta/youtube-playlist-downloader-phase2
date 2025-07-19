"""
YouTube Playlist Downloader
Phase II Source Code
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Description:
This Python application provides a GUI-based solution for downloading and organizing
video files from YouTube playlists. Users can input a playlist URL, select a folder,
and initiate downloads with visual progress tracking.
Phase II Enhancements:
- Stream title-based file filtering for accurate playback order
- Reset playback index after cancellation/completion
- Daemon threading for safe shutdown
- Dual speed metrics (instantaneous & average)
- Pause/Resume download controls
- Status console for verbose feedback
- Estimated Time of Arrival (ETA) display
- "Play First Video" and "Play Next Video" controls
- Automatic playback start on first indexed video
- Responsive GUI during downloads and playback
"""

import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pytubefix import Playlist
import threading
import re

class YouTubePlaylistDownloader:
    def __init__(self, root):
        self.root = root
        self.clapper_board = "\U0001F3AC"
        self.root.title(f"{self.clapper_board} YouTube Playlist Downloader {self.clapper_board}")
        self.root.configure(bg="#87CEEB")

        self.folder_path = tk.StringVar()
        self.cancel_download = False
        self.pause_download = False
        self.video_list = []
        self.current_video_index = 0

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text=f"{self.clapper_board} YouTube Playlist Downloader {self.clapper_board}",
                 font=("Arial", 18, "bold"), bg="#87CEEB").pack(pady=10)

        validcmd = (self.root.register(self.validate_url), '%P')
        invalidcmd = (self.root.register(self.on_invalid_url),)
        tk.Label(self.root, text="Enter YouTube Playlist URL:",
                 font=("Arial", 12, "bold"), bg="#87CEEB").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.config(validate='focusout', validatecommand=validcmd, invalidcommand=invalidcmd)
        self.url_entry.pack(pady=5)

        tk.Button(self.root, text="Select Folder", command=self.select_folder,
                  font=("Arial", 12, "bold"), bg="#FFD700").pack(pady=5)
        tk.Label(self.root, textvariable=self.folder_path,
                 font=("Arial", 12, "bold"), bg="#87CEEB").pack(pady=5)

        tk.Button(self.root, text="Download Playlist", command=self.download_playlist,
                  font=("Arial", 12, "bold"), bg="#32CD32", fg="white").pack(pady=5)
        tk.Button(self.root, text="Pause/Resume", command=self.toggle_pause,
                  font=("Arial", 12, "bold"), bg="#FFA500", fg="white").pack(pady=5)
        tk.Button(self.root, text="Cancel Download", command=self.cancel_download_action,
                  font=("Arial", 12, "bold"), bg="#FF4500", fg="white").pack(pady=5)
        tk.Button(self.root, text="Play First Video", command=self.play_first_video,
                  font=("Arial", 12, "bold"), bg="#1E90FF", fg="white").pack(pady=5)
        tk.Button(self.root, text="Play Next Video", command=self.play_next_video,
                  font=("Arial", 12, "bold"), bg="#8A2BE2", fg="white").pack(pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor="#D3D3D3", background="#32CD32", thickness=20)
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300,
                                            mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)

        self.speed_label = tk.Label(self.root, text="Speed: 0 MB/s (instant), 0 MB/s (avg)",
                                    font=("Arial", 12, "bold"), bg="#87CEEB")
        self.speed_label.pack(pady=5)
        self.time_label = tk.Label(self.root, text="Estimated Time Left: 0 seconds",
                                   font=("Arial", 12, "bold"), bg="#87CEEB")
        self.time_label.pack(pady=5)

        self.console = scrolledtext.ScrolledText(self.root, height=8, width=60, wrap=tk.WORD,
                                                 font=("Arial", 10), bg="white", state="disabled")
        self.console.pack(pady=10)

        tk.Label(self.root, text="© CMSC 495 6982 Computer Science Capstone - Group 3",
                 font=("Arial", 10, "italic"), bg="#87CEEB").pack(pady=10)

    def log_message(self, msg):
        self.console.config(state="normal")
        self.console.insert(tk.END, f"{msg}\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")
    
    def validate_url(self, value):
        regex = r'(https?://)?(www\.|m\.)?(youtube\.com|youtu\.be)/(playlist\?list=|watch\?.*?&list=)([a-zA-Z0-9_-]+)'
        if re.fullmatch(regex, value) is None:
            return False
        self.url_entry.config(highlightthickness=0)
        return True
    
    def on_invalid_url(self):
        self.url_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)

    def toggle_pause(self):
        self.pause_download = not self.pause_download
        state = "Paused" if self.pause_download else "Resumed"
        self.log_message(f"Download {state}.")

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def cancel_download_action(self):
        self.cancel_download = True
        self.current_video_index = 0
        self.log_message("Download canceled.")
        messagebox.showinfo(f"{self.clapper_board} Canceled", "Download canceled!")

    def play_video_by_index(self, index):
        path = self.folder_path.get()
        if not path:
            messagebox.showerror(f"{self.clapper_board} Error", "Please select a download folder first.")
            return

        files = sorted([f for f in os.listdir(path) if f.endswith(".mp4")])
        if 0 <= index < len(files):
            os.startfile(os.path.join(path, files[index]))
        else:
            messagebox.showerror(f"{self.clapper_board} Error", "No more videos to play.")

    def play_first_video(self):
        self.current_video_index = 0
        self.play_video_by_index(self.current_video_index)

    def play_next_video(self):
        self.current_video_index += 1
        self.play_video_by_index(self.current_video_index)

    def download_playlist(self):
        self.cancel_download = False
        self.pause_download = False
        self.video_list = []
        self.current_video_index = 0

        url = self.url_entry.get()
        path = self.folder_path.get()

        if not url or not path:
            messagebox.showerror(f"{self.clapper_board} Error", "Please provide both URL and folder.")
            return

        try:
            playlist = Playlist(url)
            count = len(playlist.video_urls)
            self.progress_bar["maximum"] = count
            self.log_message(f"Starting download for playlist: '{playlist.title}'")
            messagebox.showinfo(f"{self.clapper_board} Downloading", f"Downloading playlist: '{playlist.title}'")

            def download_videos():
                total_downloaded = 0
                start_all = time.time()

                for i, video in enumerate(playlist.videos):
                    if self.cancel_download:
                        break

                    while self.pause_download:
                        time.sleep(0.5)

                    try:
                        t0 = time.time()
                        stream = video.streams.filter(progressive=True, file_extension="mp4").first()
                        filename = f"{i:03d}_{video.title[:40].strip().replace(' ', '_')}.mp4"
                        filepath = stream.download(output_path=path, filename=filename)
                        t1 = time.time()

                        size = os.path.getsize(filepath) / (1024 * 1024)
                        total_downloaded += size
                        duration = max(t1 - t0, 0.01)
                        speed_now = size / duration
                        avg_speed = total_downloaded / max(time.time() - start_all, 0.01)
                        remaining = (count - (i + 1)) * size / max(avg_speed, 0.01)

                        self.progress_bar["value"] = i + 1
                        self.speed_label.config(text=f"Speed: {speed_now:.2f} MB/s (instant), {avg_speed:.2f} MB/s (avg)")
                        self.time_label.config(text=f"Estimated Time Left: {remaining:.1f} sec")
                        self.log_message(f"Downloaded '{filename}' at {speed_now:.2f} MB/s")
                        self.root.update_idletasks()

                        if i == 0:
                            os.startfile(filepath)

                    except Exception as e:
                        error_msg = f"Error downloading '{video.title}': {e}"
                        self.log_message(error_msg)
                        messagebox.showerror(f"{self.clapper_board} Download Error", error_msg)

                if not self.cancel_download:
                    self.current_video_index = 0
                    self.log_message("Download completed successfully.")
                    messagebox.showinfo(f"{self.clapper_board} Success", f"Download complete!\nFiles saved to '{path}'.")

            threading.Thread(target=download_videos, daemon=True).start()

        except Exception as e:
            self.log_message(f"Failed to process playlist: {e}")
            messagebox.showerror(f"{self.clapper_board} Error", f"Failed to process playlist:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubePlaylistDownloader(root)
    root.mainloop()
