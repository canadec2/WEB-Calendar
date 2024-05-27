import hashlib
import json
import sqlite3
import sqlite_query
from flask import request, session, jsonify, Response
from http import HTTPStatus
from pathlib import Path
from src.models import User

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_USERS_PATH = BASE_DIR / "data.db"


def Hashing(data):
    return hashlib.sha256(data.encode()).hexdigest()


def registration(body):
    conn = sqlite3.connect(DATA_USERS_PATH)
    cur = conn.cursor()
    data = request.get_json()

    hashed_email = Hashing(data["email"])
    hashed_password = Hashing(data["password"])

    user = User(
        data["username"],
        hashed_email,
        hashed_password,
    )

    

    cur.execute(sqlite_query.check_user_email_exists, (user.email,))
    is_exists = cur.fetchone()[0]

    if is_exists:
        return (
            jsonify(
                {"message": "Аккаунт с такой электронной почтой уже существует."}
            ),
            HTTPStatus.BAD_REQUEST,
        )

    cur.execute(
        sqlite_query.insert_user,
        (
            user.username,
            user.email,
            user._User__password,
        ),
    )

    user_id = cur.lastrowid
    session["user_id"] = user_id

    body = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
    }

    conn.commit()
    cur.close()

    return jsonify(body), HTTPStatus.CREATED


def Entrance(body):
    data = request.get_json()

    hashed_email = Hashing(data["email"])
    hashed_password = Hashing(data["password"])

    with sqlite3.connect(DATA_USERS_PATH) as conn:
        cur = conn.cursor()

        cur.execute(sqlite_query.check_user_email_exists, (hashed_email,))
        is_email_exists = cur.fetchone()[0]

        cur.execute(sqlite_query.check_user, (hashed_email, hashed_password))
        rows = cur.fetchone()

        if not rows:
            return (
                jsonify({"message": "Неверный адрес электронной почты или логин."}),
                HTTPStatus.BAD_REQUEST,
            )

        cur_id, cur_username, cur_email, cur_password = (
            rows[0],
            rows[1],
            rows[2],
            rows[3],
        )

        if is_email_exists:
            if hashed_password == cur_password:
                body = {
                    "user_id": cur_id,
                    "username": cur_username,
                    "email": cur_email,
                    "password": cur_password,
                }

                return Response(
                    json.dumps(body), HTTPStatus.OK, mimetype="application/json"
                )
            return jsonify({"message": "Неверный пароль."}), HTTPStatus.BAD_REQUEST
    return (
        jsonify({"message": "Неверный адрес электронной почты."}),
        HTTPStatus.BAD_REQUEST,
    )
