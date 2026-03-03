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
    updated = False
    for user in list(data.keys()):
        expire = datetime.fromisoformat(data[user])
        if now >= expire:
            del data[user]
            updated = True
    if updated:
        save_data(data)
    return data

@app.route("/add/<username>/<hours>")
def add_user(username, hours):
    data = load_data()
    data = clean_expired(data)

    expire_time = datetime.utcnow() + timedelta(hours=float(hours))
    data[username] = expire_time.isoformat()

    save_data(data)
    return jsonify({"status": "added"})

@app.route("/check/<username>")
def check_user(username):
    data = load_data()
    data = clean_expired(data)

    if username in data:
        return jsonify({"allowed": True})

    return jsonify({"allowed": False})

@app.route("/remove/<username>")
def remove_user(username):
    data = load_data()
    if username in data:
        del data[username]
        save_data(data)
        return jsonify({"status": "removed"})
    return jsonify({"status": "not_found"})

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
