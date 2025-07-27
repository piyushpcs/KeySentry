#This script generates a secure key for encryption and saves it to key.key

from cryptography.fernet import Fernet

# Generate a random encryption key
key = Fernet.generate_key()

# Save the key into a file so other scripts can use it
with open("key.key", "wb") as key_file:
    key_file.write(key)

print("🔐 Encryption key generated and saved as key.key")