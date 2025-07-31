# Generates a Fernet encryption key and securely saves it to a file.
# Used by the keylogger to encrypt captured keystrokes.

import os
import stat
import argparse
from cryptography.fernet import Fernet

def generate_key():
    """Generate a new 32-byte Fernet encryption key."""
    return Fernet.generate_key()

def save_key(key: bytes, filepath: str, force: bool = False):
    """
    Save the key to the specified file.
    - If the file already exists and force is False, raise an error.
    - Set file permissions to owner read/write only (chmod 600).
    """
    if os.path.exists(filepath) and not force:
        raise FileExistsError(f"File {filepath!r} already exists. Use --force to overwrite.")

    with open(filepath, "wb") as f:
        f.write(key)

    # Secure the file: read/write for owner only (Unix-style)
    os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="🔐 Generate a Fernet encryption key and save it securely."
    )
    parser.add_argument(
        "-o", "--output",
        default="key.key",
        help="Output file path for the key (default: key.key)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing key file if it already exists"
    )
    args = parser.parse_args()

    # Generate and save key
    key = generate_key()
    try:
        save_key(key, args.output, force=args.force)
    except FileExistsError as e:
        print(f"⚠️  {e}")
        return

    print(f"✅ Encryption key generated and saved to '{args.output}'")
    print("Permissions set to 600 (owner read/write only)")

if __name__ == "__main__":
    main()
