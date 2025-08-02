# KeySentry: An Encrypted Keylogger Proof-of-Concept

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🔴 Disclaimer: This tool is intended for educational and ethical research purposes only. Using this software to monitor a computer system without the explicit authorization of its owner is illegal. The author is not responsible for any damage or misuse of this software.**

## Project Overview

KeySentry is a proof-of-concept (PoC) keylogger developed to demonstrate the end-to-end lifecycle of a data capture attack. The project's core logic is organized into a clean Python package for maintainability. It showcases keystroke capture (`pynput`), real-time AES encryption (`cryptography`), and simulated data exfiltration to a local Flask server. The entire system is designed for ease of use, allowing it to be started with a single command.

## Project Structure

The project uses a standard package structure to keep the codebase organized:

```
KeySentry/
├── keysentry/ # The main Python package
│ ├── init.py # Makes 'keysentry' a package
│ ├── keylogger.py
│ ├── dashboard.py
│ ├── decrypt.py
│ └── keygen.py
├── launcher.py # The main launcher script
├── requirements.txt
├── README.md
└── .gitignore
```
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
│    dashboard.py   ├────►│ received_logs/ │
└────────────────┘     └────────────────┘
```

## Features

-   🚀 **One-Command Launcher**: The top-level `start.py` script starts and gracefully stops all components (server and keylogger) with a single command.
-   📦 **Packaged Codebase**: Core logic is neatly organized into the `keysentry` package, promoting code reusability and maintainability.
-   🔐 **Secure Key Generation**: Uses `cryptography.fernet` to generate a key and sets file permissions to `600` (owner read/write only) for security.
-   ⌨️ **Real-time Keystroke Logging**: Captures both alphanumeric characters and special keys using `pynput`.
-   🛡️ **Strong Encryption**: Encrypts every log entry with a timestamp using a symmetric Fernet (AES) key.
-   💾 **Dual Logging Mechanism**: Stores encrypted logs both locally and remotely via simulated exfiltration.
-   🛑 **Clean Kill Switch**: The project can be safely terminated via `Ctrl+C` in the launcher terminal.
-   🔓 **Decryption Utility**: A standalone script to decrypt and view the captured logs.

---

## Getting Started

Follow these instructions to get the project running on your local machine.

### 1. Prerequisites

-   Python 3.x
-   Clone the repository and navigate into the root directory.

### 2. Installation

Install the required dependencies from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
Use code with caution.

### 3. How to Run the Project

The entire project is controlled from the root KeySentry/ directory.

#### Step 1: Generate the Encryption Key

Run the keygen module from within the keysentry package using Python's -m flag. This only needs to be done once.

 ```bash
python -m keysentry.keygen
```
This will create a key.key file in the root directory.

### Step 2: Launch the Entire Project

Use the start.py script from the root directory to run the server and keylogger simultaneously.

```bash
python launcher.py
```
This will start the Flask server and the keylogger as background processes. The project is now active and capturing data.
To stop everything, simply press Ctrl+C in the terminal where the launcher is running.

### Step 3: Decrypt and View Local Logs

After stopping the project, you can decrypt the locally stored log file using the decrypt module.

```bash
python -m keysentry.decrypt
```
This will print the decrypted, timestamped keystrokes to your terminal, verifying that the entire process worked correctly.

## Ethical Use

This project is published for educational purposes only. It demonstrates concepts that are often used in malware, but it is provided to help developers and security professionals understand and defend against such threats.

-  ✅ DO use this code on systems you own and have explicit permission to test on.
-  ✅ DO use this to learn about process monitoring, encryption, and data transmission.
-  ❌ DO NOT deploy this on any system without permission.
-  ❌ DO NOT use this for any malicious or illegal activities.

Responsible disclosure and ethical boundaries are paramount.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.