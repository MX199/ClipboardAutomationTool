import tkinter as tk
from tkinter import ttk
import threading
import keyboard
import time
import pyperclip
import json

class ClipboardSenderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Clipboard Automation Tool")
        self.master.configure(bg='#f0f0f0')

        self.hotkey = self.load_hotkey()
        self.recorded_hotkey = tk.StringVar(value=self.hotkey)
        self.is_recording_hotkey = False

        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Helvetica', 14))
        style.configure('TLabel', padding=5, font=('Helvetica', 14))
        style.configure('TEntry', padding=5, font=('Helvetica', 14))

        self.send_button = tk.Button(master, text="Send Copied Text", command=self.send_copied_text, font=('Helvetica', 14))
        self.send_button.pack(pady=10)

        self.settings_button = tk.Button(master, text="Settings", command=self.open_settings, font=('Helvetica', 14))
        self.settings_button.pack(pady=10)

        self.hotkey_entry = tk.Entry(master, textvariable=self.recorded_hotkey, state='readonly', font=('Helvetica', 14))
        self.hotkey_entry.pack(pady=10)

        self.keyboard_thread_stop_event = threading.Event()
        self.keyboard_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        self.keyboard_thread.start()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.fade_in_effect()

    def fade_in_effect(self, delay=30, alpha=0):
        if alpha < 1:
            alpha += 0.05
            self.master.attributes("-alpha", alpha)
            self.master.after(delay, lambda: self.fade_in_effect(delay, alpha))
        else:
            self.master.attributes("-alpha", 1)

    def start_keyboard_listener(self):
        try:
            while not self.keyboard_thread_stop_event.is_set():
                if self.is_recording_hotkey:
                    recorded_event = keyboard.read_hotkey(suppress=False)
                    self.recorded_hotkey.set(recorded_event)
                    self.register_hotkey()
                    self.is_recording_hotkey = False
                else:
                    current_keys = [key for key in keyboard._pressed_events if isinstance(key, keyboard.KeyboardEvent)]
                    if any(isinstance(key, keyboard.KeyboardEvent) and key.name in ('ctrl', 'shift') for key in current_keys):
                        next_key = keyboard.read_key()
                        if next_key:
                            combined_hotkey = f"{'+'.join(key.name for key in current_keys)}{next_key}"
                            self.send_copied_text()
                time.sleep(0)
        except Exception as e:
            print(f"Exception in keyboard listener thread: {e}")

    def on_close(self):
        self.keyboard_thread_stop_event.set()
        self.master.destroy()

    def send_copied_text(self):
        clipboard_content = pyperclip.paste()
        keyboard.press_and_release(self.hotkey)

        # Check if the clipboard content contains newline characters
        if '\n' in clipboard_content:
            # Split the content into lines and press Shift+Enter after each line
            lines = clipboard_content.split('\n')
            for line in lines:
                keyboard.write(line)
                keyboard.press('shift')
                keyboard.press_and_release('enter')
                keyboard.release('shift')
        else:
            # If there's no newline, simulate holding Shift and pressing Enter
            keyboard.press('shift')
            keyboard.press_and_release('enter')
            keyboard.release('shift')

    def register_hotkey(self):
        keyboard.add_hotkey(self.hotkey, self.send_copied_text)

    def unregister_hotkey(self):
        keyboard.unhook_all()

    def open_settings(self):
        self.unregister_hotkey()
        self.is_recording_hotkey = True

        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        self.settings_window.configure(bg='#f0f0f0')

        hotkey_label = tk.Label(self.settings_window, text="Recorded Hotkey:")
        hotkey_label.pack(padx=5, pady=5)

        hotkey_display = tk.Label(self.settings_window, textvariable=self.recorded_hotkey)
        hotkey_display.pack(padx=5, pady=5)

        save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        self.hotkey = self.recorded_hotkey.get()
        self.register_hotkey()
        self.is_recording_hotkey = False
        self.master.focus_set()
        self.save_hotkey()
        self.settings_window.destroy()

    def load_hotkey(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            return config['hotkey']
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return "F10"

    def save_hotkey(self):
        with open('config.json', 'w') as f:
            json.dump({'hotkey': self.hotkey}, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardSenderApp(root)
    root.mainloop()
