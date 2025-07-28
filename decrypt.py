# 🔓 Decrypts encrypted keylog.txt file using Fernet key
# Prints decrypted keystrokes with timestamps

from cryptography.fernet import Fernet
import base64

# Step 1: Load the encryption key from key.key
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    print("❌ key.key file not found. Run keygen.py first.")
    exit()

fernet = Fernet(key)

# Step 2: Read encrypted keylog file
try:
    with open("keylog.txt", "rb") as log_file:
        lines = log_file.readlines()
except FileNotFoundError:
    print("❌ keylog.txt not found. Run keylogger.py first.")
    exit()

# Step 3: Decrypt each line and print
print("\n🔓 Decrypted Keylog:\n")

for line in lines:
    try:
        # Clean and decode each line from base64
        encrypted_data = base64.b64decode(line.strip())

        # Decrypt using Fernet
        decrypted_data = fernet.decrypt(encrypted_data)

        # Decode bytes to readable string
        print(decrypted_data.decode())
    except Exception as e:
        print(f"[!] Error decrypting a line: {e}")
