class User:

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.__password = password

    def get_password(self):
        return self.__password

    def __str__(self):
        return f"Пользователь {self.username} с электронной почтой {self.email}."


class Event:

    def __init__(
        self, user_id, event_name, description, year, month, day, time, periodicity
    ):
        self.user_id = user_id
        self.event_name = event_name
        self.description = description
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.periodicity = periodicity

    def get_event_info(self):
        return {
            "user_id": self.user_id,
            "event_name": self.event_name,
            "description": self.description,
            "year": self.year,
            "month": self.month,
            "week": self.week,
            "day": self.day,
            "time": self.time,
            "periodicity": self.periodicity,
        }
