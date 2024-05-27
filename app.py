from flask import Flask, request, jsonify, redirect, render_template
from http import HTTPStatus
import connexion
import os
import sys
import sqlite3
import sqlite_query
from pathlib import Path
from src.registration import registration, Entrance


# секретный ключ
def generate_secret_key():
    return os.urandom(24)

def init_db():
    with sqlite3.connect(DATA_USERS_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sqlite_query.create_table_users)
        cur.execute(sqlite_query.create_table_events)
        conn.commit()


BASE_DIR = Path(__file__).resolve().parent
DATA_USERS_PATH = os.path.join(BASE_DIR, "data.db")

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# установка ключа
app.app.secret_key = generate_secret_key()

# создаем базу данных, если ее еще нет
conn = sqlite3.connect(DATA_USERS_PATH)
cur = conn.cursor()
cur.execute(sqlite_query.create_table_users)
cur.execute(sqlite_query.create_table_events)


@app.route("/")
def index():
    return render_template("authorization.html")  # главное окно с формой



@app.route('/calendar.html')
def calendar():
    return render_template('calendar.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8086)
