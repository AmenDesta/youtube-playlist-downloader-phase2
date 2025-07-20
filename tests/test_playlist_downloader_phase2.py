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

import os
import unittest
import tkinter as tk
import sys
from unittest import skipIf
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playlist_downloader_phase2 import YouTubePlaylistDownloader

# Detect if running in GitHub Actions (headless environment)
is_ci = os.environ.get("CI") == "true"

class TestPhase2Downloader(unittest.TestCase):
    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the GUI window during test
        self.clapper_board = "\U0001F3AC"
        self.app = YouTubePlaylistDownloader(self.root)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    @patch('tkinter.messagebox.showerror')
    def test_download_playlist_missing_inputs(self, mock_showerror):
        # Simulated behavior for missing input validation
        self.app.playlist_url = ""
        self.app.folder_path = tk.StringVar()
        self.app.download_playlist()
        mock_showerror.assert_called_with(f"{self.clapper_board} Error", 'Please provide both URL and folder.')

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_log_message_appends_text(self):
        test_message = "Test123"
        self.app.log_message(test_message)
        console_content = self.app.console.get("1.0", "end").strip()
        self.assertIn(test_message, console_content)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_pause_resume_toggle(self):
        self.app.pause_download = False
        # Toggle pause
        self.app.toggle_pause()
        self.assertTrue(self.app.pause_download)
        # Toggle again
        self.app.toggle_pause()
        self.assertFalse(self.app.pause_download)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    @patch('os.startfile')
    @patch('os.listdir', return_value=['video1.mp4', 'video2.mp4', 'video3.mp4'])
    def test_play_first_video_starts_correct_file(self, mock_listdir, mock_startfile):
        self.app.folder_path.set('C:/valid-directory')
        self.app.play_first_video()
        mock_startfile.assert_called_with(os.path.join('C:/valid-directory', 'video1.mp4'))

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    @patch('os.startfile')
    @patch('os.listdir', return_value=['video1.mp4', 'video2.mp4', 'video3.mp4'])
    def test_play_next_video_starts_correct_file(self, mock_listdir, mock_startfile):
        self.app.folder_path.set('C:/valid-directory')
        self.app.current_video_index = 0
        self.app.play_next_video()
        mock_startfile.assert_called_with(os.path.join('C:/valid-directory', 'video2.mp4'))

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    @patch('tkinter.messagebox.showinfo')
    def test_playback_index_reset_on_cancel(self, mock_showinfo):
        self.app.current_video_index = 5
        self.app.cancel_download_action()
        self.assertEqual(self.app.current_video_index, 0)
        mock_showinfo.assert_called_with(f"{self.clapper_board} Canceled", 'Download canceled!')

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    @patch('tkinter.filedialog.askdirectory', return_value='/downloads/my_playlist')
    def test_select_folder_sets_path(self, mock_askdirectory):
        self.app.select_folder()
        self.assertEqual(self.app.folder_path.get(), "/downloads/my_playlist")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_validate_url(self):
        valid_urls = [
            "https://www.youtube.com/playlist?list=asdf123",
            "http://youtube.com/playlist?list=asdf123",
            "https://m.youtube.com/playlist?list=asdf123",
            "https://www.youtube.com/watch?v=abc123&list=asdf123",
            "https://youtu.be/watch?v=abc123&list=asdf123",
            "https://youtube.com/playlist?list=asdf123",
            "http://m.youtube.com/watch?v=abc123&list=asdf123",
            "https://www.youtube.com/playlist?list=asdf123_123-456",
            "https://youtube.com/watch?v=xyz987&list=asdf123"
        ]

        invalid_urls = [
            "https://www.youtube.com/watch?v=abc123",
            "https://www.google.com/playlist?list=asdf123",
            "random string",
            "https://youtube.com/playlist?list=",
            "https://youtu.be/abc123",
            "https://youtube.com/",
            "https://www.youtube.com/",
            "http://m.youtube.com/",
            ""
        ]

        for url in valid_urls:
            self.assertTrue(self.app.validate_url(url))
        for url in invalid_urls:
            self.assertFalse(self.app.validate_url(url))
        
    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def tearDown(self):
        if hasattr(self, "root"):
            self.root.destroy()

if __name__ == '__main__':
    unittest.main()
