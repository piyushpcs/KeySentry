# debug_key.py
from pynput import keyboard
import sys

print(f"🐍 Python Executable: {sys.executable}")
print("🔍 Attempting to listen to keyboard...")
print("⌨️  PLEASE TYPE SOMETHING NOW (Press ESC to quit)...")

def on_press(key):
    try:
        print(f"✅ Capture: {key.char}")
    except AttributeError:
        print(f"✅ Capture: {key}")

def on_release(key):
    if key == keyboard.Key.esc:
        print("🛑 ESC pressed. Exiting.")
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()