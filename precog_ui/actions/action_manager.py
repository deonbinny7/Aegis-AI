import os
import subprocess
from precog_ui.config import SystemMode
import pyautogui

class ActionManager:
    def __init__(self):
        # We can map component IDs or specific triggers to system actions
        self.action_map = {
            "btn_calc": self._open_calculator,
            "btn_notepad": self._open_notepad,
            "btn_vol_up": self._volume_up,
            "btn_vol_down": self._volume_down,
            "btn_media_play": self._media_play,
            "btn_media_next": self._media_next,
            "btn_media_prev": self._media_prev
        }

    def execute(self, action_id, mode: SystemMode):
        print(f"[ACTION] Triggered {action_id} in mode {mode.value}")
        
        # If the action has a registered handler
        if action_id in self.action_map:
            # We wrap in try-except so an action crash doesn't crash the UI
            try:
                self.action_map[action_id]()
            except Exception as e:
                print(f"[ACTION ERROR] {action_id} failed: {e}")
        else:
            print(f"[ACTION] No handler for {action_id}")

    def _open_calculator(self):
        print("Opening Calculator...")
        if os.name == 'nt':
            os.system("start calc")

    def _open_notepad(self):
        print("Opening Notepad...")
        if os.name == 'nt':
            os.system("start notepad")

    def _volume_up(self):
        print("Volume UP")
        pyautogui.press("volumeup")

    def _volume_down(self):
        print("Volume DOWN")
        pyautogui.press("volumedown")

    def _media_play(self):
        print("[MEDIA] Play/Pause toggled")
        pyautogui.press("playpause")

    def _media_next(self):
        print("[MEDIA] Next track")
        pyautogui.press("nexttrack")

    def _media_prev(self):
        print("[MEDIA] Previous track")
        pyautogui.press("prevtrack")

