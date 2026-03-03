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

@app.route("/add/<username>/<hours>")
def add_user(username, hours):
    data = load_data()
    expire_time = datetime.utcnow() + timedelta(hours=int(hours))
    data[username] = expire_time.isoformat()
    save_data(data)
    return jsonify({"status": "added"})

@app.route("/check/<username>")
def check_user(username):
    data = load_data()
    if username in data:
        expire = datetime.fromisoformat(data[username])
        if datetime.utcnow() < expire:
            return jsonify({"allowed": True})
        else:
            del data[username]
            save_data(data)
    return jsonify({"allowed": False})

@app.route("/")
def home():
    return "API Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)