import connexion
import os
import sys
import sqlite3
import sqlite_query
from flask import render_template, session
from http import HTTPStatus
from pathlib import Path


def generate_secret_key():
    return os.urandom(24)


def init_db():
    with sqlite3.connect(DATA_USERS_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sqlite_query.create_table_users)
        cur.execute(sqlite_query.create_table_events)
        conn.commit()


BASE_DIR = Path(__file__).resolve().parent
DATA_USERS_PATH = BASE_DIR / "data.db"

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

app.app.secret_key = generate_secret_key()

init_db()

if __name__ == "__main__":
    app.run("app:app", port=8000)
