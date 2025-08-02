import subprocess
import sys
import time

# --- Configuration ---
# Use sys.executable to ensure we use the same python interpreter
PYTHON_EXECUTABLE = sys.executable
SERVER_SCRIPT = "keysentry/dashboard.py"
KEYLOGGER_SCRIPT = "keysentry/keylogger.py"

def main():
    """
    Launches the server and keylogger as concurrent subprocesses.
    Waits for user interruption to terminate them gracefully.
    """
    print(" Starting the project...")

    # Start the server process in the background
    try:
        print(f"[*] Launching server: {SERVER_SCRIPT}")
        server_process = subprocess.Popen([PYTHON_EXECUTABLE, SERVER_SCRIPT])
        print(f"✅ Server started successfully (PID: {server_process.pid}).")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {SERVER_SCRIPT}. Make sure it's in the same directory.")
        return
    except Exception as e:
        print(f"❌ ERROR: Failed to start server: {e}")
        return

    # Give the server a moment to start up before launching the keylogger
    time.sleep(2)

    # Start the keylogger process in the background
    try:
        print(f"[*] Launching keylogger: {KEYLOGGER_SCRIPT}")
        keylogger_process = subprocess.Popen([PYTHON_EXECUTABLE, KEYLOGGER_SCRIPT])
        print(f"✅ Keylogger started successfully (PID: {keylogger_process.pid}).")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {KEYLOGGER_SCRIPT}. Make sure it's in the same directory.")
        server_process.terminate() # Clean up the server process
        return
    except Exception as e:
        print(f"❌ ERROR: Failed to start keylogger: {e}")
        server_process.terminate() # Clean up the server process
        return

    print("\n Project is running!")
    print("Both server and keylogger are active in the background.")
    print("Press Ctrl+C in this terminal to stop all processes.")

    try:
        # Keep the launcher script alive until it's interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all processes...")
    finally:
        # Terminate the child processes gracefully
        print("[*] Terminating keylogger...")
        keylogger_process.terminate()
        print("[*] Terminating server...")
        server_process.terminate()
        print("✅ All processes have been stopped. Exiting.")

if __name__ == "__main__":
    main()