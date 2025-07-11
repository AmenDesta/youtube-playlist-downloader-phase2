YouTube Playlist Downloader – Phase II

CMSC 495 6982 Computer Science Capstone – Group 3 Last Updated: July 2025 
License: Educational use only

Project Description

This Python-based desktop application enables users to download and play entire YouTube playlists with ease. Built using pytubefix and tkinter, the program emphasizes modular design, user-friendly interface, responsive execution, and robust error handling.

Phase I Features

* Graphical interface to enter YouTube playlist URLs
* Folder selection for download location
* Real-time progress bar to track downloads
* Multithreaded downloads for smooth UI performance
* Cancel download functionality
* Automatic playback of the first downloaded .mp4 file

Phase II Enhancements

* Stream title-based filename generation to preserve playlist order
* Playback index reset after cancellation or completion
* Daemon threading to ensure clean exit of background processes
* Dual download speed display: instantaneous and average metrics
* Pause and resume capability for long downloads
* Status console for live, scrollable logs and diagnostics

Technologies Used

Python 3.x

tkinter for GUI interface

pytubefix for playlist parsing and video streams

threading, os, time for concurrency and system operations

How to Run

1. Install Required Package Open a terminal and install the required Python library:

bash

pip install pytubefix

2. Launch the Application Run the script from your terminal or preferred Python environment:

bash

python playlist_downloader_phase2.py

3. Using the Interface

* Paste a valid YouTube playlist URL into the input field.
* Click Select Folder to choose where videos will be saved.
* Press Download Playlist to begin downloading videos.
* Use Pause/Resume and Cancel Download to manage active downloads.
* After download, use Play First Video or Play Next Video for playback.
* Monitor progress, speed, estimated time, and status messages via the live console and progress bar.

Authors

Group 3 – Summer 2025 University of Maryland Global Campus Developed for the CMSC 495 Capstone Course

License

For academic and educational use only. Redistribution or commercial use is prohibited.
