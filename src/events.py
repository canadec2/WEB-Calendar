from pathlib import Path
import sqlite3
import sqlite_query
from flask import request, jsonify
from src.models import Event
from http import HTTPStatus


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_EVENTS_PATH = BASE_DIR / "data.db"


def create_event(body):
    conn = sqlite3.connect(DATA_EVENTS_PATH)
    cur = conn.cursor()
    cur.execute(sqlite_query.create_table_events)
    conn.commit()
    conn.commit()

    event_data = request.get_json()

    user_id = event_data["user_id"]
    name = event_data["event_name"]
    description = event_data["event_description"]
    year = event_data["year"]
    month = event_data["month"]
    day = event_data["day"]
    start_time = event_data["start_time"]
    end_time = event_data["end_time"]
    periodicity = event_data["periodicity"]

    new_event = Event(
        user_id,
        name,
        description,
        year,
        month,
        day,
        start_time,
        end_time,
        periodicity,
    )

    cur.execute(
        sqlite_query.insert_events,
        (
            new_event.user_id,
            new_event.event_name,
            new_event.description,
            new_event.year,
            new_event.month,
            new_event.day,
            new_event.start_time,
            new_event.end_time,
            new_event.periodicity,
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    return (
        jsonify(
            {
                "message": "Событие успешно создано",
                "event": {
                    "name": name,
                    "description": description,
                    "year": year,
                    "month": month,
                    "day": day,
                    "start_time": start_time,
                    "end_time": end_time,
                    "periodicity": periodicity,
                },
            }
        ),
        HTTPStatus.CREATED,
    )


def get_user_events_by_id(user_id):
    try:
        conn = sqlite3.connect(DATA_EVENTS_PATH)
        cur = conn.cursor()
        cur.execute(
            sqlite_query.get_events,
            (user_id,),
        )
        events = cur.fetchall()
        cur.close()
        conn.close()

        if not events:
            return (
                jsonify({"message": "Не найдены события для данного пользователя."}),
                HTTPStatus.NOT_FOUND,
            )

        event = [
            {
                "event_name": event[0],
                "description": event[1],
                "year": event[2],
                "month": event[3],
                "day": event[4],
                "start_time": event[5],
                "end_time": event[6],
                "periodicity": event[7],
            }
            for event in events
        ]
        return jsonify(event), HTTPStatus.OK

    except sqlite3.Error as e:
        return (
            jsonify({"message": f"Ошибка базы данных: {e}"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def delete_event_by_id(event_id):
    try:
        conn = sqlite3.connect(DATA_EVENTS_PATH)
        cur = conn.cursor()
        cur.execute(sqlite_query.delete_events, (event_id,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Событие успешно удалено."}), HTTPStatus.OK

    except sqlite3.Error as e:
        return (
            jsonify({"message": f"Ошибка базы данных: {e}"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def update_event_date(event_id, new_date):
    try:
        conn = sqlite3.connect(DATA_EVENTS_PATH)
        cur = conn.cursor()

        cur.execute(sqlite_query.select_id_event, (event_id,))
        event = cur.fetchone()

        if not event:
            return (
                jsonify({"message": "Событие не найдено."}),
                HTTPStatus.NOT_FOUND,
            )

        day, month, year = new_date.split("-")

        cur.execute(
            sqlite_query.update_date_event,
            (
                day,
                month,
                year,
                event_id,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()

        return (
            jsonify({"message": "Дата события успешно обновлена."}),
            HTTPStatus.OK,
        )

    except sqlite3.Error as e:
        return (
            jsonify({"message": f"Ошибка базы данных: {e}"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def update_event_time(event_id, new_start_time, new_end_time):
    try:
        conn = sqlite3.connect(DATA_EVENTS_PATH)
        cur = conn.cursor()

        cur.execute(sqlite_query.select_id_event, (event_id,))
        event = cur.fetchone()

        if not event:
            return (
                jsonify({"message": "Событие не найдено."}),
                HTTPStatus.NOT_FOUND,
            )

        cur.execute(
            sqlite_query.update_time_event,
            (new_start_time, new_end_time, event_id),
        )
        conn.commit()
        cur.close()
        conn.close()

        return (
            jsonify({"message": "Время события успешно обновлено."}),
            HTTPStatus.OK,
        )

    except sqlite3.Error as e:
        return (
            jsonify({"message": f"Ошибка базы данных: {e}"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
