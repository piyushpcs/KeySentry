# Keylogger with Encrypted Data Exfiltration 

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🔴 Disclaimer: This tool is intended for educational and ethical research purposes only. Using this software to monitor a computer system without the explicit authorization of its owner is illegal. The author is not responsible for any damage or misuse of this software.**

## Project Overview

This project is a proof-of-concept (PoC) demonstrating a keylogger with a complete execution cycle:
1.  **Secure Key Generation**: Creates a strong, unique encryption key.
2.  **Keystroke Capture**: Logs all keystrokes.
3.  **Real-time Encryption**: Encrypts logs immediately upon capture.
4.  **Local & Remote Logging**: Stores logs locally and simulates exfiltration to a remote server.
5.  **Decryption Utility**: Provides a tool to decrypt and view the captured logs.

The goal is to provide a clear, hands-on understanding of the mechanics behind data capture, encryption, and exfiltration for cybersecurity students, developers, and ethical hackers. The project is designed for ease of use, allowing the entire system to be started with a single command.

## Project Flowchart

This diagram illustrates how the different scripts in the project interact with each other.

```
┌────────────────┐     ┌───────────┐     ┌────────────────┐
│   keygen.py    ├────►│  key.key  │◄────┤   decrypt.py   │
└────────────────┘     └───────────┘     └────────────────┘
                           ▲                      ▲
                           │                      │
┌────────────────┐         │                ┌──────────────┐
│  keylogger.py  ├─────────┘                │ .keylog.txt  │
└────────────────┘                          └──────────────┘
       │     │                                    ▲
       │     └────────────────────────────────────┘
       │                      (Writes encrypted, base64-encoded logs)
       │
       │ (Sends encrypted data via HTTP POST)
       ▼
┌────────────────┐     ┌────────────────┐
│    server.py   ├────►│ received_logs/ │
└────────────────┘     └────────────────┘
```

## Features

-   🚀 **One-Command Launcher**: A convenient launcher script (`main.py`) starts and gracefully stops all components (server and keylogger) with a single command.
-   🔐 **Secure Key Generation**: Uses `cryptography.fernet` to generate a key and sets file permissions to `600` (owner read/write only) for security.
-   ⌨️ **Real-time Keystroke Logging**: Captures both alphanumeric characters and special keys (e.g., `[space]`, `[ctrl]`) using `pynput`.
-   🛡️ **Strong Encryption**: Encrypts every log entry with a timestamp using a symmetric Fernet (AES) key.
-   💾 **Dual Logging Mechanism**:
    -   **Local**: Saves encrypted and base64-encoded logs to a hidden file (`.keylog.txt`).
    -   **Remote**: Simulates data exfiltration by sending encrypted logs to a Flask server via HTTP POST.
-   🚀 **Simulated C2 Server**: A simple Flask server that listens for incoming logs and saves them to a `received_logs` directory.
-   🛑 **Clean Kill Switch**: The keylogger can be safely terminated by pressing the `Esc` key, or through the main launcher's `Ctrl+C` command.
-   🔓 **Decryption Utility**: A standalone script (`decrypt.py`) to read, decode, and display the contents of the local log file.

---

## Getting Started

Follow these instructions to get the project running on your local machine for development and testing.

### 1. Prerequisites

-   Python 3.x
-   The required Python libraries can be installed from `requirements.txt`.

First, create a `requirements.txt` file with the following content:
```
# requirements.txt
pynput
cryptography
requests
Flask
```

Then, install the dependencies:
```bash
pip install -r requirements.txt
```

### 2. File Structure

It is highly recommended to create a `.gitignore` file to prevent sensitive files (like the encryption key and logs) from being committed to Git.

```
# .gitignore

# Python cache
__pycache__/
*.pyc

# Sensitive files - DO NOT COMMIT
key.key
*.key
.keylog.txt
received_logs/

# Virtual environment
venv/
```

### 3. How to Run the Project

The entire project can now be controlled from a single terminal.

#### Step 1: Generate the Encryption Key

In your terminal, run the `keygen.py` script. This only needs to be done once.

```bash
python keygen.py
```
This will create a `key.key` file in your directory.

#### Step 2: Launch the Entire Project

Use the `main.py` script to start the server and the keylogger simultaneously.

```bash
python launcher.py
```
This will start the Flask server and then the keylogger as background processes. You will see status messages confirming that both have been launched. The project is now active and capturing data.

To stop everything, simply press **`Ctrl+C`** in the terminal where the launcher is running. It will gracefully terminate both the server and the keylogger.

#### Step 3: Decrypt and View Local Logs

After you have stopped the project, you can decrypt the locally stored log file (`.keylog.txt`) using the `decrypt.py` script.

```bash
python decrypt.py
```
This will print the decrypted, timestamped keystrokes to your terminal, verifying that the entire process worked correctly.

## Ethical Use

This project is published for educational purposes only. It demonstrates concepts that are often used in malware, but it is provided to help developers and security professionals understand and defend against such threats.

-   ✅ **DO** use this code on systems you own and have explicit permission to test on.
-   ✅ **DO** use this to learn about process monitoring, encryption, and data transmission.
-   ❌ **DO NOT** deploy this on any system without permission.
-   ❌ **DO NOT** use this for any malicious or illegal activities.

Responsible disclosure and ethical boundaries are paramount.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.