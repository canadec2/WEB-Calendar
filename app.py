import connexion
import requests
from flask import render_template

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


@app.route("/")
def home():
    response = requests.get("http://127.0.0.1:8000/api/events", timeout=5)
    if response.status_code == 200:
        calendar_data = response.json()
    else:
        calendar_data = []
    return render_template("home.html", data=calendar_data)


if __name__ == "__main__":
    app.run("app:app", port=8000)
