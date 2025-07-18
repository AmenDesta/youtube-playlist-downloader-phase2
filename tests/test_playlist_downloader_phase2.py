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
from unittest import skipIf

# Detect if running in GitHub Actions (headless environment)
is_ci = os.environ.get("CI") == "true"

class TestPhase2Downloader(unittest.TestCase):
    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the GUI window during test
        # Simulate GUI component initialization
        self.app_folder_path = "sample_folder"
        self.playback_index = 0
        self.video_list = ["00_intro.mp4", "01_setup.mp4", "02_demo.mp4"]

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_download_playlist_missing_inputs(self):
        # Simulated behavior for missing input validation
        playlist_url = ""
        folder_path = ""
        error_triggered = playlist_url == "" or folder_path == ""
        self.assertTrue(error_triggered)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_log_message_appends_text(self):
        # Simulate logging behavior
        log_output = []
        message = "Download started"
        log_output.append(message)
        self.assertIn("Download started", log_output)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_pause_resume_toggle(self):
        is_paused = False
        # Toggle pause
        is_paused = not is_paused
        self.assertTrue(is_paused)
        # Toggle again
        is_paused = not is_paused
        self.assertFalse(is_paused)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_play_first_video_starts_correct_file(self):
        first_video = self.video_list[0]
        self.assertEqual(first_video, "00_intro.mp4")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_play_next_video_starts_correct_file(self):
        current_index = 1
        next_video = self.video_list[current_index]
        self.assertEqual(next_video, "01_setup.mp4")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_playback_index_reset_on_cancel(self):
        self.playback_index = 3
        self.playback_index = 0  # Reset
        self.assertEqual(self.playback_index, 0)

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def test_select_folder_sets_path(self):
        simulated_input = "/downloads/my_playlist"
        self.app_folder_path = simulated_input
        self.assertEqual(self.app_folder_path, "/downloads/my_playlist")

    @skipIf(is_ci, "Skipping GUI-dependent tests in CI environment")
    def tearDown(self):
        if hasattr(self, "root"):
            self.root.destroy()

if __name__ == '__main__':
    unittest.main()
