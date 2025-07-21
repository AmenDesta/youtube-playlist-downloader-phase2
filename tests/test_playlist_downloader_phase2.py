"""
YouTube Playlist Downloader – Phase II Enhanced Test Suite
CMSC 495 6982 Computer Science Capstone – Group 3
-------------------------------------------------
Functional unit tests for playlist_downloader_phase2.py:
• GUI logic and setup
• Folder selection and playback flow
• Pause/resume, cancel, logging
• URL validation with extensive coverage
Last Updated: July 2025
"""

import os
import sys
import unittest
import tkinter as tk
from unittest import skipIf
from unittest.mock import patch

# Support direct execution (if test run manually)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playlist_downloader_phase2 import YouTubePlaylistDownloader

is_ci = os.environ.get("CI") == "true"

class TestPhase2Downloader(unittest.TestCase):
    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    """Initialize the test GUI app instance and set required attributes."""
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = YouTubePlaylistDownloader(self.root)
        self.clapper_board = "\U0001F3AC"

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("tkinter.messagebox.showerror")
    def test_download_playlist_missing_inputs(self, mock_showerror):
        """Verify error message displays when URL or folder input is missing."""
        self.app.url_entry.delete(0, tk.END)
        self.app.folder_path.set("")
        self.app.download_playlist()
        mock_showerror.assert_called_with(f"{self.clapper_board} Error", "Please provide both URL and folder.")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_log_message_writes_to_console(self):
        """Check that log_message correctly appends content to the console widget."""
        message = "Download started"
        self.app.log_message(message)
        content = self.app.console.get("1.0", tk.END)
        self.assertIn(message, content)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_pause_resume_toggle_changes_state(self):
        """Ensure toggle_pause correctly flips pause_download state."""
        self.app.pause_download = False
        self.app.toggle_pause()
        self.assertTrue(self.app.pause_download)
        self.app.toggle_pause()
        self.assertFalse(self.app.pause_download)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("os.startfile")
    @patch("os.listdir", return_value=["video1.mp4", "video2.mp4", "video3.mp4"])
    def test_play_first_video_starts_correct_file(self, mock_listdir, mock_startfile):
        """Verify that play_first_video launches the first file in the folder."""
        self.app.folder_path.set("/mock/path")
        self.app.play_first_video()
        mock_startfile.assert_called_with(os.path.join("/mock/path", "video1.mp4"))

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("os.startfile")
    @patch("os.listdir", return_value=["video1.mp4", "video2.mp4", "video3.mp4"])
    def test_play_next_video_starts_correct_file(self, mock_listdir, mock_startfile):
        """Validate that play_next_video launches the correct file based on index."""
        self.app.folder_path.set("/mock/path")
        self.app.current_video_index = 1
        self.app.play_next_video()
        mock_startfile.assert_called_with(os.path.join("/mock/path", "video3.mp4"))

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("tkinter.messagebox.showinfo")
    def test_cancel_download_resets_state(self, mock_info):
        """Confirm cancel_download_action resets index and shows confirmation."""
        self.app.current_video_index = 3
        self.app.cancel_download_action()
        self.assertEqual(self.app.current_video_index, 0)
        mock_info.assert_called_with(f"{self.clapper_board} Canceled", "Download canceled!")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("tkinter.filedialog.askdirectory", return_value="/downloads/my_playlist")
    def test_select_folder_sets_path(self, mock_dialog):
        """Ensure select_folder sets folder_path correctly using filedialog."""
        self.app.select_folder()
        self.assertEqual(self.app.folder_path.get(), "/downloads/my_playlist")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_validate_url_full_range(self):
        """Exhaustively test valid and invalid YouTube playlist URLs."""
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
            self.assertTrue(self.app.validate_url(url), msg=f"Should be valid: {url}")
        for url in invalid_urls:
            self.assertFalse(self.app.validate_url(url), msg=f"Should be invalid: {url}")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def tearDown(self):
        """Clean up GUI resources after each test."""
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
