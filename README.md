# KeySentry: An Encrypted Keylogger Proof-of-Concept

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🔴 Disclaimer: This tool is intended for educational and ethical research purposes only. Using this software to monitor a computer system without the explicit authorization of its owner is illegal. The author is not responsible for any damage or misuse of this software.**

---

## Project Overview

KeySentry is a proof-of-concept (PoC) keylogger developed to demonstrate the end-to-end lifecycle of a data capture attack. The project's core logic is organized into a clean Python package for maintainability. It showcases keystroke capture (`pynput`), real-time AES encryption (`cryptography`), and simulated data exfiltration to a local Flask server.

## Project Structure
```
KeySentry/
├── keysentry/              # The main Python package
│   ├── __init__.py         # Makes 'keysentry' a package
│   ├── keylogger.py
│   ├── dashboard.py
│   ├── decrypt.py
│   └── keygen.py
├── launcher.py             # The main launcher script
├── requirements.txt
├── README.md
└── .gitignore
```
## Project Flowchart

This diagram illustrates how the different scripts in the project interact with each other.
```
┌────────────────┐      ┌───────────┐      ┌────────────────┐
│   keygen.py    ├─────►│  key.key  │◄─────┤   decrypt.py   │
└────────────────┘      └───────────┘      └────────────────┘
                            ▲                       ▲
                            │                       │
┌────────────────┐          │                 ┌──────────────┐
│  keylogger.py  ├──────────┘                 │ .keylog.txt  │
└────────────────┘                            └──────────────┘
       │      │                                     ▲
       │      └─────────────────────────────────────┘
       │                       (Writes encrypted, base64-encoded logs)
       │
       │ (Sends encrypted data via HTTP POST)
       ▼
┌────────────────┐      ┌──────────────────┐
│  dashboard.py  ├─────►│ received_logs/IP │
└────────────────┘      └──────────────────┘
```
## Features

-   🚀 **Modular Design**: Core logic is neatly organized into the `keysentry` package.
-   🔐 **Secure Key Generation**: Uses `cryptography.fernet` (AES) and sets file permissions to `600` (owner read/write only).
-   ⌨️ **Real-time Keystroke Logging**: Captures alphanumeric and special keys using `pynput`.
-   🛡️ **Strong Encryption**: Encrypts every log entry with a timestamp before saving or sending.
-   💾 **Exfiltration Simulation**: Sends encrypted logs to a local Flask C2 server on Port 5001.
-   🛑 **Clean Kill Switch**: Handles `SIGINT` (Ctrl+C) gracefully to flush buffers before exiting.

---

## Getting Started

### 1. Prerequisites
-   Python 3.x
-   Clone the repository:
    ```bash
    git clone [https://github.com/piyushpcs/KeySentry.git](https://github.com/piyushpcs/KeySentry.git)
    cd KeySentry
    ```

### 2. Installation
Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Generate Encryption Key
Run this once to create the key.key file:
```
python3 -m keysentry.keygen
```
---

## 🚀 How to Run the Project
Option A: macOS (Recommended)
Due to macOS "Input Monitoring" security restrictions, you must run the server and keylogger in two separate terminal windows.

Terminal 1 (The C2 Server):
```
source venv/bin/activate
python3 keysentry/dashboard.py
```
Terminal 2 (The Keylogger):
```
source venv/bin/activate
python3 keysentry/keylogger.py
```
Note: You must grant "Input Monitoring" permission to Terminal in System Settings > Privacy & Security. If it fails, restart Terminal.

Option B: Linux / Windows
You can use the automated launcher to start both processes at once:
```
python3 launcher.py
```
### 🔓 Decrypting Logs
The server organizes logs by IP address in the received_logs directory. To decrypt them:
```
# Syntax: python -m keysentry.decrypt <path_to_log_folder>
python3 -m keysentry.decrypt received_logs/127.0.0.1
```
---
## Ethical Use
✅ DO use this code on systems you own and have explicit permission to test on.

❌ DO NOT deploy this on any system without permission.

❌ DO NOT use this for any malicious or illegal activities.

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
