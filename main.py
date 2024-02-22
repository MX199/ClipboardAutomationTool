import tkinter as tk
import pyperclip
import pyautogui
import keyboard

def type_clipboard():
    clipboard_text = pyperclip.paste()  # Get text from clipboard
    pyautogui.typewrite(clipboard_text)  # Simulate typing

def change_hotkey():
    global current_hotkey, previous_hotkey
    current_hotkey = hotkey_entry.get()  # Get the hotkey entered by the user
    keyboard.remove_hotkey(previous_hotkey)  # Remove the previous hotkey
    keyboard.add_hotkey(current_hotkey, type_clipboard)  # Set the new hotkey
    previous_hotkey = current_hotkey  # Update the previous hotkey

def main():
    global previous_hotkey, current_hotkey, hotkey_entry
    previous_hotkey = 'f11'  # Default hotkey
    current_hotkey = 'f11'

    # Initialize Tkinter
    root = tk.Tk()
    root.title("Clipboard Typer")

    # Add label
    label = tk.Label(root, text="Press the hotkey to type the copied text.\nPress 'Ctrl + C' to exit.")
    label.pack(pady=10)

    # Add entry field for hotkey
    hotkey_label = tk.Label(root, text="Enter new hotkey:")
    hotkey_label.pack()
    hotkey_entry = tk.Entry(root)
    hotkey_entry.insert(0, current_hotkey)
    hotkey_entry.pack()

    # Add button to change hotkey
    change_button = tk.Button(root, text="Change Hotkey", command=change_hotkey)
    change_button.pack(pady=5)

    # Add F11 hotkey
    keyboard.add_hotkey(current_hotkey, type_clipboard)

    # Run Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
