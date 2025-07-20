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

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import os
from playlist_downloader_phase2 import YouTubePlaylistDownloader

# CI-safe check to skip GUI tests
is_ci = os.environ.get("CI") == "true"

class TestPlaylistDownloaderPhase2(unittest.TestCase):

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = YouTubePlaylistDownloader(self.root)

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_toggle_pause_changes_state_and_logs(self):
        with patch.object(self.app, "log_message") as mock_log:
            self.app.pause_download = False
            self.app.toggle_pause()
            self.assertTrue(self.app.pause_download)
            mock_log.assert_called_with("Download Paused.")
            self.app.toggle_pause()
            self.assertFalse(self.app.pause_download)
            mock_log.assert_called_with("Download Resumed.")

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("playlist_downloader_phase2.filedialog.askdirectory", return_value="/mock/path")
    def test_select_folder_sets_value(self, mock_dialog):
        self.app.select_folder()
        self.assertEqual(self.app.folder_path.get(), "/mock/path")

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("playlist_downloader_phase2.messagebox.showerror")
    def test_play_video_by_index_no_folder(self, mock_error):
        self.app.folder_path.set("")
        self.app.play_video_by_index(0)
        mock_error.assert_called_once()

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_cancel_download_resets_state(self):
        with patch.object(self.app, "log_message") as mock_log, \
             patch("playlist_downloader_phase2.messagebox.showinfo") as mock_info:
            self.app.cancel_download_action()
            self.assertTrue(self.app.cancel_download)
            self.assertEqual(self.app.current_video_index, 0)
            mock_log.assert_called_with("Download canceled.")
            mock_info.assert_called_once()

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("playlist_downloader_phase2.os.listdir", return_value=["00_intro.mp4", "01_demo.mp4", "02_summary.mp4"])
    @patch("playlist_downloader_phase2.os.startfile")
    def test_play_first_video_opens_correct_file(self, mock_startfile, mock_listdir):
        self.app.folder_path.set("/mock/path")
        self.app.play_first_video()
        mock_startfile.assert_called_with("/mock/path/00_intro.mp4")

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    @patch("playlist_downloader_phase2.os.listdir", return_value=["00_intro.mp4", "01_demo.mp4", "02_summary.mp4"])
    @patch("playlist_downloader_phase2.os.startfile")
    def test_play_next_video_opens_correct_file(self, mock_startfile, mock_listdir):
        self.app.folder_path.set("/mock/path")
        self.app.current_video_index = 1
        self.app.play_next_video()
        mock_startfile.assert_called_with("/mock/path/02_summary.mp4")

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_validate_url_full_range(self):
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

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def test_log_message_writes_to_console(self):
        msg = "Download started"
        self.app.log_message(msg)
        content = self.app.console.get("1.0", tk.END)
        self.assertIn(msg, content)

    @unittest.skipIf(is_ci, "Skipping GUI-dependent tests in CI")
    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
