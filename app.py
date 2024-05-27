from flask import render_template, session, jsonify
from http import HTTPStatus
import connexion
import os
import sys
import sqlite3
import sqlite_query
from pathlib import Path


# секретный ключ
def generate_secret_key():
    return os.urandom(24)

BASE_DIR = Path(__file__).resolve().parent
DATA_EVENTS_PATH = os.path.join(BASE_DIR, "data.db")

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# установка ключа
app.app.secret_key = generate_secret_key()

conn = sqlite3.connect(DATA_EVENTS_PATH)  # создаем базу данных, если ее еще нет
cur = conn.cursor()

@app.route("/")
def index():
    return render_template("authorization.html")  # главное окно с формой

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8086)
