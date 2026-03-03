from flask import Flask, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = "users.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def clean_expired(data):
    now = datetime.utcnow()
    changed = False

    for user in list(data.keys()):
        last_seen = datetime.fromisoformat(data[user])
        if now - last_seen > timedelta(seconds=10):
            del data[user]
            changed = True

    if changed:
        save_data(data)

    return data

@app.route("/heartbeat/<username>")
def heartbeat(username):
    data = load_data()
    data = clean_expired(data)

    data[username] = datetime.utcnow().isoformat()
    save_data(data)

    return jsonify({"status": "online"})

@app.route("/check/<username>")
def check_user(username):
    data = load_data()
    data = clean_expired(data)

    return jsonify({"allowed": username in data})

@app.route("/clear")
def clear_all():
    save_data({})
    return jsonify({"status": "cleared"})

@app.route("/")
def home():
    return "API Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
