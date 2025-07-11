"""
YouTube Playlist Downloader Test
Phase II Source Code
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Description:
Unit tests for core functionality of the Phase II playlist downloader script.

Last Updated: July 2025
License: For educational use only.
"""

import unittest
from unittest.mock import patch
import tkinter as tk
import os
import sys

# Adjust path to find the Phase II script
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playlist_downloader_phase2 import YouTubePlaylistDownloader

class TestPhase2Downloader(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = YouTubePlaylistDownloader(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.filedialog.askdirectory', return_value='C:/test-folder')
    def test_select_folder_sets_path(self, mock_ask):
        self.app.select_folder()
        self.assertEqual(self.app.folder_path.get(), 'C:/test-folder')

    def test_pause_resume_toggle(self):
        self.app.pause_download = False
        self.app.toggle_pause()
        self.assertTrue(self.app.pause_download)
        self.app.toggle_pause()
        self.assertFalse(self.app.pause_download)

    def test_playback_index_reset_on_cancel(self):
        self.app.current_video_index = 5
        with patch('tkinter.messagebox.showinfo'):
            self.app.cancel_download_action()
        self.assertEqual(self.app.current_video_index, 0)

    def test_log_message_appends_text(self):
        sample_text = "Testing log message"
        self.app.console.config(state="normal")  # unlock temporarily
        initial_length = len(self.app.console.get("1.0", tk.END))
        self.app.log_message(sample_text)
        updated_length = len(self.app.console.get("1.0", tk.END))
        self.assertGreater(updated_length, initial_length)
        self.app.console.config(state="disabled")

    @patch('os.startfile')
    @patch('os.listdir', return_value=['001_Test.mp4', '002_Demo.mp4'])
    def test_play_first_video_starts_correct_file(self, mock_listdir, mock_startfile):
        self.app.folder_path.set('C:/valid-directory')
        self.app.play_first_video()
        mock_startfile.assert_called_with(os.path.join('C:/valid-directory', '001_Test.mp4'))

    @patch('os.startfile')
    @patch('os.listdir', return_value=['001_Test.mp4', '002_Demo.mp4'])
    def test_play_next_video_starts_correct_file(self, mock_listdir, mock_startfile):
        self.app.folder_path.set('C:/valid-directory')
        self.app.current_video_index = 0
        self.app.play_next_video()
        self.assertEqual(self.app.current_video_index, 1)
        mock_startfile.assert_called_with(os.path.join('C:/valid-directory', '002_Demo.mp4'))

    @patch('tkinter.messagebox.showerror')
    def test_download_playlist_missing_inputs(self, mock_error):
        self.app.folder_path.set('')
        self.app.url_entry.delete(0, tk.END)
        self.app.download_playlist()
        mock_error.assert_called()

if __name__ == '__main__':
    unittest.main()
