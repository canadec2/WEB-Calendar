create_table_users = """CREATE TABLE IF NOT EXISTS users(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      email TEXT NOT NULL,
                      password TEXT NOT NULL
                    );"""

insert_user = """INSERT INTO users (username, email, password) VALUES (?, ?, ?);"""

select_users = """SELECT * FROM users;"""

check_user_email_exists = """SELECT EXISTS(SELECT 1 FROM users WHERE email = ?);"""

find_id = """SELECT id FROM users WHERE username = ?;"""

check_user = """SELECT * FROM users WHERE email = ? AND password = ?;"""

create_table_events = """CREATE TABLE IF NOT EXISTS events(
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_name TEXT,
                description TEXT,
                day TEXT,
                month TEXT,
                year TEXT,
                start_time TEXT,
                end_time TEXT,
                periodicity TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)

    )"""

insert_events = """INSERT INTO events (user_id, event_name, description, day, month, year, start_time, end_time, periodicity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

select_id_event = """SELECT * FROM events WHERE event_id = ?;"""

get_events = """SELECT event_name, description, day, month, year, start_time, end_time, periodicity FROM events WHERE user_id = ?;"""

delete_events = """DELETE FROM events WHERE event_id = ?;"""

update_date_event = (
    """UPDATE events SET day = ?, month = ?, year = ? WHERE event_id = ?;"""
)

update_time_event = (
    """UPDATE events SET start_time = ?, end_time = ? WHERE event_id = ?;"""
)
