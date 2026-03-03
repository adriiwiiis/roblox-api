from flask import Flask, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = "users.json"

# Cargar datos del JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Guardar datos en JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Agregar usuario
@app.route("/add/<username>/<hours>")
def add_user(username, hours):
    data = load_data()
    expire_time = datetime.utcnow() + timedelta(hours=int(hours))
    data[username] = expire_time.isoformat()
    save_data(data)
    return jsonify({"status": "added"})

# Verificar usuario
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

# Eliminar usuario
@app.route("/remove/<username>")
def remove_user(username):
    data = load_data()
    if username in data:
        del data[username]
        save_data(data)
        return jsonify({"status": "removed"})
    return jsonify({"status": "not_found"})

# Limpiar todos los usuarios
@app.route("/clear")
def clear_all():
    save_data({})
    return jsonify({"status": "cleared"})

# Home
@app.route("/")
def home():
    return "API Running"

# ⚡ Compatible con Railway (puerto dinámico)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
