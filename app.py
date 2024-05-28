import os
import sqlite3
import sys
from pathlib import Path
import connexion
from flask import render_template
import sqlite_query


def generate_secret_key():
    return os.urandom(24)


BASE_DIR = Path(__file__).resolve().parent
DATA_USERS_PATH = os.path.join(BASE_DIR, "data.db")

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

app.app.secret_key = generate_secret_key()

conn = sqlite3.connect(DATA_USERS_PATH)
cur = conn.cursor()
cur.execute(sqlite_query.create_table_users)
cur.execute(sqlite_query.create_table_events)


@app.route("/")
def index():
    return render_template("authorization.html")


@app.route("/calendar.html")
def calendar():
    return render_template("calendar.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8086)
